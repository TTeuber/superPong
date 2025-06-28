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
        self.player_manager = PlayerManager()
        
        # Initialize game entities
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Set up menu callbacks
        self.menu_system.set_callbacks(
            on_resume=self.resume_game,
            on_restart=self.reset_game,
            on_quit=self.quit_game
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
        
        # Handle pause input (single-press detection)
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
        if self.state_manager.is_playing():
            self.update_playing_mode()
        elif self.state_manager.is_aiming():
            self.update_aiming_mode()
        elif self.state_manager.is_paused():
            # Don't update game logic when paused, only particle system
            pass
        
        # Always update particle system
        self.particle_system.update()
    
    def update_playing_mode(self):
        """Update game during normal play"""
        # Update input for human player (player 0)
        paddles = self.player_manager.get_paddles()
        alive_players = self.player_manager.get_alive_players()
        
        self.input_handler.update_paddle_movement([paddles[0]])

        # Update AI players
        self.player_manager.update_ai_players(self.ball)

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
        
        if winner_info['winner'] >= 0:
            # Add victory celebration
            self.particle_system.add_victory_celebration(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_COLORS[winner_info['winner']])
        
        # Reset the game after a brief moment
        self.reset_game()

    def reset_game(self):
        """Reset the game to initial state"""
        # Reset all systems
        self.player_manager.reset()
        self.ball.reset_position()
        self.particle_system.clear()
        self.state_manager.reset()
        self.aiming_system.reset()
        self.menu_system.reset_menu()
        
        # Reset pause input state
        self.pause_key_pressed = False

    def render(self):
        """Render the game"""
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
                                 aiming_angle, aiming_timer, pause_menu_selected)
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()