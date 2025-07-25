import pygame
import random
from entities.ball import Ball
from systems.renderer import GameRenderer
from systems.input_handler import InputHandler
from systems.particle_system import ParticleSystem
from systems.game_state_manager import GameStateManager
from systems.menu_system import MenuSystem
from systems.aiming_system import AimingSystem
from systems.collision_system import CollisionSystem
from systems.player_manager import PlayerManager
from systems.start_screen_system import StartScreenSystem
from systems.game_over_system import GameOverSystem
from systems.settings_system import SettingsSystem
from systems.settings_screen_system import SettingsScreenSystem
from systems.player_count_system import PlayerCountSystem
from systems.controller_setup_system import ControllerSetupSystem
from systems.powerup_system import PowerUpSystem
from systems.powerup_renderer import PowerUpRenderer
from utils import constants

class Game:
    def __init__(self):
        pygame.init()
        
        # Initialize settings system first to get screen scale
        self.settings_system = SettingsSystem()
        screen_scale = self.settings_system.get_setting('screen_scale')
        
        # Get monitor info and calculate appropriate screen size
        info = pygame.display.Info()
        self.monitor_width = info.current_w
        self.monitor_height = info.current_h
        
        # Store monitor available size for consistent scaling
        self.monitor_available_size = min(self.monitor_width, self.monitor_height)
        
        # Calculate default size based on monitor and scale setting
        # Use the smaller dimension to maintain square aspect ratio
        available_size = self.monitor_available_size
        target_size = int(available_size * screen_scale)
        
        # Clamp to min/max sizes
        target_size = max(constants.MIN_SCREEN_SIZE, min(constants.MAX_SCREEN_SIZE, target_size))
        
        # Update global screen dimensions
        constants.update_screen_dimensions(target_size, target_size)
        
        # Create resizable window
        self.screen = pygame.display.set_mode((target_size, target_size), pygame.RESIZABLE)
        pygame.display.set_caption("4-Player Neon Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game systems
        self.renderer = GameRenderer(self.screen)
        self.input_handler = InputHandler()
        self.particle_system = ParticleSystem()
        self.state_manager = GameStateManager()
        self.menu_system = MenuSystem()
        self.aiming_system = AimingSystem()
        self.collision_system = CollisionSystem()
        # Settings system already initialized above
        self.powerup_system = PowerUpSystem(self.settings_system)
        self.powerup_renderer = PowerUpRenderer()
        
        # Link power-up system to collision system
        self.collision_system.set_powerup_system(self.powerup_system)
        
        # Get settings for other systems
        ai_difficulty = self.settings_system.get_setting('ai_difficulty')
        controller_sensitivity = self.settings_system.get_setting('controller_sensitivity')
        
        self.player_manager = PlayerManager(ai_difficulty=ai_difficulty, settings_system=self.settings_system)
        
        # Apply controller sensitivity if it's different from default
        if controller_sensitivity != constants.CONTROLLER_SENSITIVITY:
            print(f"Applying controller sensitivity: {controller_sensitivity}")
        self.start_screen_system = StartScreenSystem()
        self.game_over_system = GameOverSystem()
        self.settings_screen_system = SettingsScreenSystem()
        self.player_count_system = PlayerCountSystem()
        self.controller_setup_system = ControllerSetupSystem(self.input_handler)
        
        # Initialize game entities
        self.ball = Ball(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
        
        # Set up menu callbacks
        self.menu_system.set_callbacks(
            on_resume=self.resume_game,
            on_restart=self.restart_game,
            on_main_menu=self.go_to_start_screen,
            on_quit=self.quit_game
        )
        
        # Set up start screen callbacks
        self.start_screen_system.set_callbacks(
            on_play=self.show_player_count_selection,
            on_settings=self.show_settings
        )
        
        # Set up game over callbacks
        self.game_over_system.set_callbacks(
            on_restart=self.restart_game,
            on_main_menu=self.return_to_main_menu,
            on_quit=self.quit_game
        )
        
        # Set up settings screen callbacks
        self.settings_screen_system.set_callbacks(
            on_back=self.exit_settings,
            on_setting_changed=self.on_setting_changed
        )
        
        # Pause input handling
        self.pause_key_pressed = False  # Track pause key state for single-press detection
        self.pause_cooldown_frames = 0  # Prevent rapid pause/unpause cycles
        self.PAUSE_COOLDOWN_FRAMES = 15  # Quarter second at 60 constants.FPS
        
        # Initialization debouncing
        self.initialization_frames = 0  # Prevent input for a few frames after startup
        self.INPUT_DEBOUNCE_FRAMES = 30  # Half second at 60 constants.FPS
        
        # CRITICAL: Reset all input states to prevent auto-triggering during startup
        self.input_handler.reset_input_states()
        
        # Show controller status
        if self.input_handler.controller_connected:
            print(f"Game ready with controller: {self.input_handler.controller.get_name()}")
        else:
            print("Game ready with keyboard input")

    def resume_game(self):
        """Resume game from pause"""
        self.state_manager.resume_game()
        
    def go_to_start_screen(self):
        """Go back to start screen"""
        # Reset game entities when returning to start screen
        self.player_manager.reset()
        self.ball.reset_position()
        self.particle_system.clear()
        self.powerup_system.clear()
        self.aiming_system.reset()
        self.menu_system.reset_menu()
        self.pause_key_pressed = False
        
        # Clear all player-controller assignments
        self.input_handler.clear_player_assignments()
        
        # Reset player manager to default single-player configuration
        self.player_manager.update_player_configuration(self.player_manager._get_default_config())
        
        # Now set state to start screen
        self.state_manager.set_state(constants.GAME_STATE_START_SCREEN)
        self.start_screen_system.reset()
        
        # IMPORTANT: Force the start screen to ignore the current confirm input
        # This prevents the Enter key from pause menu selection being processed on start screen
        self.start_screen_system.menu_confirm_pressed = True
        
    def quit_game(self):
        """Quit the game"""
        self.running = False
        print("Quitting game")
        
    def start_game(self):
        """Start the main game from start screen"""
        # Reset game entities without resetting state manager
        self.player_manager.reset()
        self.ball.reset_position()
        self.particle_system.clear()
        self.powerup_system.clear()
        self.aiming_system.reset()
        self.menu_system.reset_menu()
        self.pause_key_pressed = False
        
        # Auto-assign controller 0 to player 0 in single player mode
        # Check if this is single player mode (default configuration)
        player_config = self.player_manager.player_config
        human_count = sum(1 for p in player_config if p['active'] and p['is_human'])
        
        if human_count == 1:
            # Find the human player
            human_player_id = None
            for i, config in enumerate(player_config):
                if config['active'] and config['is_human']:
                    human_player_id = i
                    break
            
            # Assign first available controller to the human player
            if human_player_id is not None and self.input_handler.controllers:
                # Get the first available controller
                first_controller = min(self.input_handler.controllers.keys())
                self.input_handler.assign_player_to_controller(human_player_id, first_controller)
                print(f"Auto-assigned controller {first_controller} to player {human_player_id}")
        
        # Now enter the game state
        self.state_manager.enter_game()
        print("Starting game")
    
    def show_player_count_selection(self):
        """Show player count selection screen"""
        self.player_count_system.reset()
        self.state_manager.enter_player_count_selection()
        print("Entering player count selection")
    
    def start_controller_setup(self, player_count):
        """Start controller setup with specified player count"""
        self.controller_setup_system.set_required_players(player_count)
        self.controller_setup_system.attempt_auto_assignment()
        self.state_manager.enter_controller_setup()
        print(f"Entering controller setup for {player_count} players")
    
    def start_multiplayer_game(self):
        """Start multiplayer game with configured players"""
        # Get player configuration from controller setup
        assignments = self.controller_setup_system.get_controller_assignments()
        
        # Check if multiplayer bots are enabled
        multiplayer_bots_enabled = self.settings_system.get_setting('multiplayer_bots_enabled')
        
        # Create player configuration for PlayerManager
        player_config = []
        for player_id in range(4):  # Always 4 slots, but not all active
            if player_id in assignments:
                config = assignments[player_id]
                player_config.append({
                    'active': True,
                    'is_human': config['is_human'],
                    'controller_index': config['controller_index']
                })
            else:
                # Check if we should fill this slot with a bot
                if multiplayer_bots_enabled:
                    # Active bot player slot
                    player_config.append({
                        'active': True,
                        'is_human': False,
                        'controller_index': None
                    })
                else:
                    # Inactive player slot
                    player_config.append({
                        'active': False,
                        'is_human': False,
                        'controller_index': None
                    })
        
        # Apply controller assignments to input handler
        for player_id, config in enumerate(player_config):
            if config['active'] and config['controller_index'] is not None:
                self.input_handler.assign_player_to_controller(player_id, config['controller_index'])
        
        # Update player manager with new configuration
        self.player_manager.update_player_configuration(player_config)
        
        # Start the game
        self.start_game()
        
    def show_settings(self):
        """Show settings screen"""
        # Load current settings into the settings screen system
        self.settings_screen_system.load_current_settings(self.settings_system)
        
        # Synchronize screen scale to ensure UI shows correct current value
        self.settings_screen_system.sync_screen_scale(self.settings_system)
        
        # Enter settings state
        self.state_manager.enter_settings()
        print("Entering settings screen")
        
    def exit_settings(self):
        """Exit settings screen and return to start screen"""
        self.state_manager.enter_start_screen()
        print("Exiting settings screen")
        
    def on_setting_changed(self, setting_key, setting_value):
        """Handle when a setting is changed"""
        self.settings_system.set_setting(setting_key, setting_value)
        
        # Apply setting changes immediately
        if setting_key == 'ai_difficulty':
            # Update existing AI player difficulties
            for ai_player in self.player_manager.get_ai_players():
                ai_player.difficulty = setting_value
            print(f"AI difficulty updated to: {setting_value}")
        elif setting_key == 'controller_sensitivity':
            print(f"Controller sensitivity updated to: {setting_value}")
            # Note: Controller sensitivity is applied from constants, 
            # so it will take effect on the next input reading
        elif setting_key == 'sound_enabled':
            print(f"Sound setting updated to: {setting_value}")
        elif setting_key == 'multiplayer_bots_enabled':
            print(f"Multiplayer bots setting updated to: {setting_value}")
            # Note: This will take effect on the next multiplayer game
        elif setting_key == 'screen_scale':
            print(f"[DEBUG] Screen scale setting changed: {setting_value}")
            print(f"[DEBUG] Current SCALE_FACTOR before change: {constants.SCALE_FACTOR}")
            # Apply the new screen scale immediately using stored monitor dimensions
            available_size = self.monitor_available_size
            target_size = int(available_size * setting_value)
            target_size = max(constants.MIN_SCREEN_SIZE, min(constants.MAX_SCREEN_SIZE, target_size))
            print(f"[DEBUG] Calculated target_size: {target_size} (monitor_available: {available_size}, scale: {setting_value})")
            
            # Update screen dimensions
            constants.update_screen_dimensions(target_size, target_size)
            print(f"[DEBUG] New SCALE_FACTOR after update: {constants.SCALE_FACTOR}")
            
            # Recreate the display
            self.screen = pygame.display.set_mode((target_size, target_size), pygame.RESIZABLE)
            self.renderer.screen = self.screen
            # Update UI fonts for new scale
            self.renderer.ui_effects.update_fonts()
            
            # Apply scale changes to all existing entities
            self.apply_scale_changes()
            # Note: Sound system will be implemented in future
            
    def apply_scale_changes(self):
        """Apply scale changes to all existing entities"""
        print(f"[DEBUG] apply_scale_changes called with constants.SCALE_FACTOR: {constants.SCALE_FACTOR}")
        
        # Update main game ball
        if hasattr(self, 'ball') and self.ball:
            old_size = self.ball.size
            self.ball.recreate_with_scale()
            print(f"[DEBUG] Main ball: size {old_size} -> {self.ball.size}")
        else:
            print(f"[DEBUG] Main ball: NOT FOUND (hasattr: {hasattr(self, 'ball')}, ball exists: {getattr(self, 'ball', None) is not None})")
        
        # Update demo ball in start screen
        if hasattr(self, 'start_screen_system') and hasattr(self.start_screen_system, 'demo_ball') and self.start_screen_system.demo_ball:
            old_size = self.start_screen_system.demo_ball.size
            self.start_screen_system.demo_ball.recreate_with_scale()
            print(f"[DEBUG] Demo ball: size {old_size} -> {self.start_screen_system.demo_ball.size}")
        else:
            print(f"[DEBUG] Demo ball: NOT FOUND")
        
        # Update all active powerups
        if hasattr(self, 'powerup_system') and self.powerup_system:
            powerups = self.powerup_system.get_powerups()
            print(f"[DEBUG] Found {len(powerups)} powerups to update")
            for i, powerup in enumerate(powerups):
                old_size = powerup.size
                powerup.recreate_with_scale()
                print(f"[DEBUG] Powerup {i}: size {old_size} -> {powerup.size}")
        else:
            print(f"[DEBUG] PowerUp system: NOT FOUND")
        
        # Update paddles in all systems that have them
        if hasattr(self, 'player_manager'):
            paddles = self.player_manager.get_paddles()
            print(f"[DEBUG] Found {len(paddles)} game paddles to update")
            for i, paddle in enumerate(paddles):
                if paddle:
                    old_width, old_height = paddle.width, paddle.height
                    paddle.recreate_with_scale()
                    print(f"[DEBUG] Game paddle {i}: size {old_width}x{old_height} -> {paddle.width}x{paddle.height}")
        else:
            print(f"[DEBUG] Player manager: NOT FOUND")
        
        # Update demo paddles in start screen
        if hasattr(self, 'start_screen_system') and hasattr(self.start_screen_system, 'demo_paddles'):
            demo_paddles = self.start_screen_system.demo_paddles
            print(f"[DEBUG] Found {len(demo_paddles)} demo paddles to update")
            for i, paddle in enumerate(demo_paddles):
                if paddle:
                    old_width, old_height = paddle.width, paddle.height
                    paddle.recreate_with_scale()
                    print(f"[DEBUG] Demo paddle {i}: size {old_width}x{old_height} -> {paddle.width}x{paddle.height}")
        else:
            print(f"[DEBUG] Start screen demo paddles: NOT FOUND")
        
        print(f"[DEBUG] apply_scale_changes completed")
        
    def restart_game(self):
        """Restart the game from game over screen"""
        print("Restarting game...")
        # Reset game entities without resetting state manager
        self.player_manager.reset()
        self.ball.reset_position()
        self.particle_system.clear()
        self.powerup_system.clear()
        self.aiming_system.reset()
        self.menu_system.reset_menu()
        self.game_over_system.reset()
        self.pause_key_pressed = False
        
        # Enter game state
        self.state_manager.enter_game()
        
    def return_to_main_menu(self):
        """Return to the start screen from game over"""
        print("Returning to main menu...")
        # Reset all systems
        self.player_manager.reset()
        self.ball.reset_position()
        self.particle_system.clear()
        self.powerup_system.clear()
        self.aiming_system.reset()
        self.menu_system.reset_menu()
        self.game_over_system.reset()
        self.start_screen_system.reset()
        self.pause_key_pressed = False
        
        # Clear all player-controller assignments
        self.input_handler.clear_player_assignments()
        
        # Reset player manager to default single-player configuration
        self.player_manager.update_player_configuration(self.player_manager._get_default_config())
        
        # CRITICAL: Reset input handler to prevent input leakage
        # This prevents the Enter press from game over menu being processed again on start screen
        self.input_handler.reset_input_states()
        
        # Enter start screen state
        self.state_manager.enter_start_screen()

    def handle_events(self):
        """Handle pygame events"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize - maintain square aspect ratio
                new_size = min(event.w, event.h)
                new_size = max(constants.MIN_SCREEN_SIZE, min(constants.MAX_SCREEN_SIZE, new_size))
                
                # Update global screen dimensions
                constants.update_screen_dimensions(new_size, new_size)
                
                # Recreate the display surface with new size
                self.screen = pygame.display.set_mode((new_size, new_size), pygame.RESIZABLE)
                
                # Update renderer with new screen
                self.renderer.screen = self.screen
                # Update UI fonts for new scale
                self.renderer.ui_effects.update_fonts()
                
                # Apply scale changes to all existing entities
                self.apply_scale_changes()
                
                # Update screen scale in settings based on monitor dimensions
                available_size = self.monitor_available_size
                new_scale = new_size / available_size
                new_scale = max(0.5, min(1.5, new_scale))  # Clamp to valid range
                self.settings_system.set_setting('screen_scale', new_scale)
                
                # Sync the settings screen system with the new scale
                self.settings_screen_system.sync_screen_scale(self.settings_system)

        # Update input handler
        self.input_handler.handle_events(events)
        
        # Increment initialization frame counter
        if self.initialization_frames < self.INPUT_DEBOUNCE_FRAMES:
            self.initialization_frames += 1
            return  # Skip all input processing during debounce period
        
        # Handle input based on current state
        if self.state_manager.is_start_screen():
            # Handle start screen input
            self.start_screen_system.handle_start_menu_input(self.input_handler)
        elif self.state_manager.is_settings():
            # Handle settings screen input
            self.settings_screen_system.handle_settings_input(self.input_handler)
        elif self.state_manager.is_player_count_selection():
            # Handle player count selection input
            self.handle_player_count_input()
        elif self.state_manager.is_controller_setup():
            # Handle controller setup input
            self.handle_controller_setup_input()
        elif self.state_manager.is_game_over():
            # Handle game over input
            self.game_over_system.handle_game_over_input(self.input_handler)
        else:
            # Handle pause input (single-press detection) - only during gameplay
            pause_action_taken = False
            
            # Decrement pause cooldown
            if self.pause_cooldown_frames > 0:
                self.pause_cooldown_frames -= 1
            
            # Only process pause input if cooldown has expired
            if self.input_handler.is_pause_pressed() and self.pause_cooldown_frames == 0:
                if not self.pause_key_pressed:  # Only trigger on initial press
                    # Mark both escape and space as used for pause to prevent menu actions
                    if self.input_handler.escape_just_pressed:
                        self.input_handler.mark_escape_used_for_pause()
                    if self.input_handler.space_just_pressed:
                        self.input_handler.mark_space_used_for_pause()
                    
                    if not self.state_manager.is_paused():
                        self.state_manager.toggle_pause()
                        self.menu_system.reset_menu()
                        pause_action_taken = True
                        self.pause_cooldown_frames = self.PAUSE_COOLDOWN_FRAMES  # Start cooldown
                    else:
                        # If already paused, quick resume with pause button
                        self.resume_game()
                        pause_action_taken = True
                        self.pause_cooldown_frames = self.PAUSE_COOLDOWN_FRAMES  # Start cooldown
                    self.pause_key_pressed = True
            elif not self.input_handler.is_pause_pressed():
                self.pause_key_pressed = False
                
            # Handle pause menu navigation (only when paused and no pause action was taken this frame)
            if self.state_manager.is_paused() and not pause_action_taken:
                self.menu_system.handle_pause_menu_input(self.input_handler)

    def handle_player_count_input(self):
        """Handle input for player count selection screen"""
        # Navigation
        nav_direction = self.input_handler.get_menu_navigation()
        if nav_direction != 0:
            if nav_direction > 0:
                self.player_count_system.navigate_down()
            else:
                self.player_count_system.navigate_up()
        
        # Selection (with single-press detection)
        result = self.player_count_system.handle_input(self.input_handler)
        if result:
            if result == "start_single_player":
                # Start single player game directly
                self.start_game()
            elif result == "start_controller_setup":
                # Move to controller setup
                player_count = self.player_count_system.get_player_count()
                self.start_controller_setup(player_count)
            elif result == "enter_multiplayer_selection":
                # Just stay in player count selection (it updates internally)
                pass
        
        # Back button
        if self.input_handler.is_menu_cancel_pressed():
            result = self.player_count_system.go_back()
            if result == "back_to_main_menu":
                self.state_manager.enter_start_screen()

    def handle_controller_setup_input(self):
        """Handle input for controller setup screen"""
        # Update controller setup system (handles A button presses)
        self.controller_setup_system.update()
        
        # Check if all players are ready
        if self.controller_setup_system.are_all_players_ready():
            # Auto-start game when everyone is ready
            self.start_multiplayer_game()
        
        # Back button
        if self.input_handler.is_menu_cancel_pressed():
            self.state_manager.enter_player_count_selection()

    def update(self):
        """Update game state based on current mode"""
        if self.state_manager.is_start_screen():
            self.update_start_screen()
        elif self.state_manager.is_settings():
            self.update_settings()
        elif self.state_manager.is_player_count_selection():
            # Update player count system for debouncing
            self.player_count_system.update()
        elif self.state_manager.is_controller_setup():
            # Controller setup system is updated in input handling
            pass
        elif self.state_manager.is_game_over():
            self.update_game_over()
        elif self.state_manager.is_playing():
            self.update_playing_mode()
        elif self.state_manager.is_aiming():
            self.update_aiming_mode()
        elif self.state_manager.is_paused():
            # Don't update game logic when paused, only particle system
            pass
        
        # Always update particle system (except on start screen, settings, player count, controller setup, and game over)
        if (not self.state_manager.is_start_screen() and 
            not self.state_manager.is_settings() and 
            not self.state_manager.is_player_count_selection() and
            not self.state_manager.is_controller_setup() and
            not self.state_manager.is_game_over()):
            self.particle_system.update()
    
    def update_start_screen(self):
        """Update start screen demo game"""
        self.start_screen_system.update_demo_game()
    
    def update_settings(self):
        """Update settings screen"""
        # Settings screen doesn't need game logic updates, just input handling
        pass
    
    def update_game_over(self):
        """Update game over screen effects"""
        self.game_over_system.update()
    
    def update_playing_mode(self):
        """Update game during normal play"""
        # Update input for all human players
        paddles = self.player_manager.get_paddles()
        alive_players = self.player_manager.get_alive_players()
        
        # Get all human players and their paddles
        human_players = self.player_manager.get_human_players()
        human_paddles = []
        
        for player_id in human_players:
            if player_id < len(paddles) and alive_players[player_id] and paddles[player_id] is not None:
                # Apply control scrambling if active (for now, only affects original Player 0)
                if player_id == 0:
                    target_player_id = self.powerup_system.get_scrambled_player_id(0)
                    if target_player_id < len(paddles) and paddles[target_player_id] is not None:
                        human_paddles.append(paddles[target_player_id])
                    elif paddles[player_id] is not None:
                        human_paddles.append(paddles[player_id])
                else:
                    # Other human players get normal input (no scrambling for now)
                    human_paddles.append(paddles[player_id])
        
        # Update input for all human players at once
        if human_paddles:
            self.input_handler.update_paddle_movement(human_paddles)

        # Update AI players
        self.player_manager.update_ai_players(self.ball)
        
        # Update power-up system
        self.powerup_system.update()
        
        # Check for pending paddle swap
        swap_player = self.powerup_system.get_pending_paddle_swap()
        if swap_player >= 0:
            self.execute_paddle_swap(swap_player, alive_players)
        
        # Check power-up collection (ball-based)
        collected = self.powerup_system.check_ball_collection(self.ball, alive_players)
        if collected:
            # Add collection particle effect at ball position
            self.powerup_renderer.render_collection_effect(
                self.particle_system, self.ball.x, self.ball.y, collected['type']
            )
            
        # Apply power-up effects to paddles
        for i, paddle in enumerate(paddles):
            if paddle is not None:
                size_modifier = self.powerup_system.get_paddle_size_modifier(i, list(range(4)))
                paddle.apply_size_modifier(size_modifier)
            
        # Apply power-up effects to ball
        ball_speed_modifier = self.powerup_system.get_ball_speed_modifier()
        self.ball.apply_speed_modifier(ball_speed_modifier)
        
        # Apply magnetic forces from magnetized paddles
        self.powerup_system.apply_magnetic_force(self.ball, paddles)
        
        # Apply chaos power-up effects
        # Wild bounce effect
        wild_bounce_occurred = self.powerup_system.apply_wild_bounce(self.ball)
        if wild_bounce_occurred:
            # Create visual effect for wild bounce
            self.powerup_renderer.render_wild_bounce_effect(
                self.particle_system, self.ball.x, self.ball.y
            )

        # Update paddles
        self.player_manager.update_paddles()

        # Update ball
        self.ball.update()
        
        # Update decoy balls
        decoy_balls = self.powerup_system.get_decoy_balls()
        for decoy_ball in decoy_balls:
            decoy_ball.update()

        # Check ball-paddle collisions
        self.collision_system.check_ball_paddle_collisions(
            self.ball, paddles, alive_players, self.particle_system, self.renderer
        )
        
        # Check decoy ball-paddle collisions (they bounce but don't affect scoring)
        for decoy_ball in decoy_balls:
            self.collision_system.check_ball_paddle_collisions(
                decoy_ball, paddles, alive_players, self.particle_system, self.renderer
            )

        # Check for boundary collisions and handle life loss
        collision_info = self.collision_system.check_ball_boundary_collisions(
            self.ball, alive_players, self.particle_system, self.renderer
        )
        
        if collision_info['life_lost']:
            self.handle_life_loss(collision_info['player_hit'])
            
        # Check decoy ball boundary collisions (they just bounce off walls)
        for decoy_ball in decoy_balls:
            self.collision_system.check_ball_boundary_collisions(
                decoy_ball, alive_players, self.particle_system, self.renderer, 
                force_bounce=True  # Force decoy balls to bounce off walls
            )
    
    def update_aiming_mode(self):
        """Update game during aiming phase"""
        paddles = self.player_manager.get_paddles()
        alive_players = self.player_manager.get_alive_players()
        
        # Update aiming system
        should_launch = self.aiming_system.update_aiming_mode(
            paddles, alive_players, self.input_handler, self.player_manager
        )
        
        # Launch ball when timer expires
        if should_launch:
            self.aiming_system.launch_ball(self.ball)
            
            # Check for immediate power-up collection from aimed shot
            collected = self.powerup_system.check_ball_collection(self.ball, alive_players)
            if collected:
                # Add collection particle effect at ball position
                self.powerup_renderer.render_collection_effect(
                    self.particle_system, self.ball.x, self.ball.y, collected['type']
                )
                
            self.state_manager.enter_playing_mode()
            
    def handle_life_loss(self, player_id):
        """Handle a player losing a life"""
        result = self.player_manager.lose_life(player_id)
        
        if result['eliminated']:
            # Add dramatic elimination particle effect
            self.particle_system.add_elimination_effect(
                constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2, constants.PLAYER_COLORS[player_id])
            
            # Strong screen shake for elimination
            self.renderer.add_screen_shake(10, 20)
            
            # Just reset ball for eliminated player
            self.ball.reset_position()
            
            if result['game_over']:
                self.game_over()
        else:
            # Player lost life but is still alive - enter aiming mode
            self.renderer.add_screen_shake(6, 15)
            alive_players = self.player_manager.get_alive_players()
            self.aiming_system.enter_aiming_mode(player_id, self.ball, alive_players)
            self.state_manager.enter_aiming_mode()


    def game_over(self):
        """Handle game over state"""
        winner_info = self.player_manager.get_winner_info()
        
        print(winner_info['message'])
        
        # Set winner information for game over system
        self.game_over_system.set_winner_info(
            winner_info['winner'],
            winner_info['lives_remaining'],
            winner_info['message']
        )
        
        if winner_info['winner'] >= 0:
            # Add victory celebration
            self.particle_system.add_victory_celebration(
                constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2, constants.PLAYER_COLORS[winner_info['winner']])
        
        # Enter game over state instead of resetting immediately
        self.state_manager.enter_game_over()

    def reset_game(self):
        """Reset the game to initial state"""
        # Reset all systems
        self.player_manager.reset()
        self.ball.reset_position()
        self.particle_system.clear()
        self.powerup_system.clear()
        self.state_manager.reset()
        self.aiming_system.reset()
        self.menu_system.reset_menu()
        
        # Reset pause input state
        self.pause_key_pressed = False

    def render(self):
        """Render the game"""
        if self.state_manager.is_start_screen():
            # Render start screen
            self.renderer.render_start_screen(self.start_screen_system)
        elif self.state_manager.is_settings():
            # Render settings screen
            self.renderer.render_settings_screen(self.settings_screen_system)
        elif self.state_manager.is_player_count_selection():
            # Render player count selection screen
            self.renderer.render_player_count_screen(self.player_count_system)
        elif self.state_manager.is_controller_setup():
            # Render controller setup screen
            self.renderer.render_controller_setup_screen(self.controller_setup_system)
        elif self.state_manager.is_game_over():
            # Render game over screen
            self.renderer.render_game_over_screen(self.game_over_system)
        else:
            # Get data from systems
            paddles = self.player_manager.get_paddles()
            lives = self.player_manager.get_lives()
            alive_players = self.player_manager.get_alive_players()
            game_state = self.state_manager.get_current_state()
            aiming_player = self.aiming_system.get_aiming_player()
            aiming_angle = self.aiming_system.get_aiming_angle()
            aiming_timer = self.aiming_system.get_aiming_timer()
            pause_menu_selected = self.menu_system.get_selected_option()
            
            self.renderer.render_frame(paddles, self.ball, lives, alive_players, 
                                     self.particle_system, game_state, aiming_player, 
                                     aiming_angle, aiming_timer, pause_menu_selected,
                                     self.powerup_system, self.powerup_renderer)
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(constants.FPS)

        pygame.quit()
        
    def execute_paddle_swap(self, player_id, alive_players):
        """Execute paddle swap between player and random opponent"""
        # Get list of other alive players
        other_players = [i for i in range(4) if i != player_id and alive_players[i]]
        
        if not other_players:
            return  # No one to swap with
            
        # Choose random opponent
        opponent_id = random.choice(other_players)
        
        # Get paddles
        paddles = self.player_manager.get_paddles()
        player_paddle = paddles[player_id]
        opponent_paddle = paddles[opponent_id]
        
        # Make sure both paddles exist
        if player_paddle is None or opponent_paddle is None:
            return
        
        # Swap positions
        temp_x, temp_y = player_paddle.x, player_paddle.y
        player_paddle.x, player_paddle.y = opponent_paddle.x, opponent_paddle.y
        opponent_paddle.x, opponent_paddle.y = temp_x, temp_y
        
        # Add visual effect
        self.particle_system.add_particle(
            player_paddle.x, player_paddle.y, 0, 0, constants.NEON_ORANGE, 60
        )
        self.particle_system.add_particle(
            opponent_paddle.x, opponent_paddle.y, 0, 0, constants.NEON_ORANGE, 60
        )
        
        print(f"Player {player_id} swapped with Player {opponent_id}")