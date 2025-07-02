import pygame
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
from systems.powerup_system import PowerUpSystem
from systems.powerup_renderer import PowerUpRenderer
from utils.constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        self.powerup_system = PowerUpSystem()
        self.powerup_renderer = PowerUpRenderer()
        
        # Link power-up system to collision system
        self.collision_system.set_powerup_system(self.powerup_system)
        
        # Initialize settings system first to get settings
        self.settings_system = SettingsSystem()
        ai_difficulty = self.settings_system.get_setting('ai_difficulty')
        controller_sensitivity = self.settings_system.get_setting('controller_sensitivity')
        
        self.player_manager = PlayerManager(ai_difficulty=ai_difficulty)
        
        # Apply controller sensitivity if it's different from default
        if controller_sensitivity != CONTROLLER_SENSITIVITY:
            print(f"Applying controller sensitivity: {controller_sensitivity}")
        self.start_screen_system = StartScreenSystem()
        self.game_over_system = GameOverSystem()
        self.settings_screen_system = SettingsScreenSystem()
        
        # Initialize game entities
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Set up menu callbacks
        self.menu_system.set_callbacks(
            on_resume=self.resume_game,
            on_restart=self.restart_game,
            on_quit=self.quit_game
        )
        
        # Set up start screen callbacks
        self.start_screen_system.set_callbacks(
            on_play=self.start_game,
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
        
        # Show controller status
        if self.input_handler.controller_connected:
            print(f"Game ready with controller: {self.input_handler.controller.get_name()}")
        else:
            print("Game ready with keyboard input")

    def resume_game(self):
        """Resume game from pause"""
        self.state_manager.resume_game()
        
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
        
        # Now enter the game state
        self.state_manager.enter_game()
        print("Starting game")
        
    def show_settings(self):
        """Show settings screen"""
        # Load current settings into the settings screen system
        self.settings_screen_system.load_current_settings(self.settings_system)
        
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
            # Note: Sound system will be implemented in future
        
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
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()

        # Update input handler
        self.input_handler.handle_events(events)
        
        # Handle input based on current state
        if self.state_manager.is_start_screen():
            # Handle start screen input
            self.start_screen_system.handle_start_menu_input(self.input_handler)
        elif self.state_manager.is_settings():
            # Handle settings screen input
            self.settings_screen_system.handle_settings_input(self.input_handler)
        elif self.state_manager.is_game_over():
            # Handle game over input
            self.game_over_system.handle_game_over_input(self.input_handler)
        else:
            # Handle pause input (single-press detection) - only during gameplay
            if self.input_handler.is_pause_pressed():
                if not self.pause_key_pressed:  # Only trigger on initial press
                    if not self.state_manager.is_paused():
                        self.state_manager.toggle_pause()
                        self.menu_system.reset_menu()
                    else:
                        # If already paused, quick resume with pause button
                        self.resume_game()
                    self.pause_key_pressed = True
            else:
                self.pause_key_pressed = False
                
            # Handle pause menu navigation (only when paused)
            if self.state_manager.is_paused():
                self.menu_system.handle_pause_menu_input(self.input_handler)


    def update(self):
        """Update game state based on current mode"""
        if self.state_manager.is_start_screen():
            self.update_start_screen()
        elif self.state_manager.is_settings():
            self.update_settings()
        elif self.state_manager.is_game_over():
            self.update_game_over()
        elif self.state_manager.is_playing():
            self.update_playing_mode()
        elif self.state_manager.is_aiming():
            self.update_aiming_mode()
        elif self.state_manager.is_paused():
            # Don't update game logic when paused, only particle system
            pass
        
        # Always update particle system (except on start screen, settings, and game over)
        if not self.state_manager.is_start_screen() and not self.state_manager.is_settings() and not self.state_manager.is_game_over():
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
        # Update input for human player (player 0)
        paddles = self.player_manager.get_paddles()
        alive_players = self.player_manager.get_alive_players()
        
        self.input_handler.update_paddle_movement([paddles[0]])

        # Update AI players
        self.player_manager.update_ai_players(self.ball)
        
        # Update power-up system
        self.powerup_system.update()
        
        # Check power-up collection (ball-based)
        collected = self.powerup_system.check_ball_collection(self.ball, alive_players)
        if collected:
            # Add collection particle effect at ball position
            self.powerup_renderer.render_collection_effect(
                self.particle_system, self.ball.x, self.ball.y, collected['type']
            )
            
        # Apply power-up effects to paddles
        for i, paddle in enumerate(paddles):
            size_modifier = self.powerup_system.get_paddle_size_modifier(i, list(range(4)))
            paddle.apply_size_modifier(size_modifier)
            
        # Apply power-up effects to ball
        ball_speed_modifier = self.powerup_system.get_ball_speed_modifier()
        self.ball.apply_speed_modifier(ball_speed_modifier)

        # Update paddles
        self.player_manager.update_paddles()

        # Update ball
        self.ball.update()

        # Check ball-paddle collisions
        self.collision_system.check_ball_paddle_collisions(
            self.ball, paddles, alive_players, self.particle_system, self.renderer
        )

        # Check for boundary collisions and handle life loss
        collision_info = self.collision_system.check_ball_boundary_collisions(
            self.ball, alive_players, self.particle_system, self.renderer
        )
        
        if collision_info['life_lost']:
            self.handle_life_loss(collision_info['player_hit'])
    
    def update_aiming_mode(self):
        """Update game during aiming phase"""
        paddles = self.player_manager.get_paddles()
        alive_players = self.player_manager.get_alive_players()
        
        # Update aiming system
        should_launch = self.aiming_system.update_aiming_mode(
            paddles, alive_players, self.input_handler
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
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_COLORS[player_id])
            
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
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_COLORS[winner_info['winner']])
        
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
            self.clock.tick(FPS)

        pygame.quit()