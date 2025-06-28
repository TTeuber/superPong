import pygame
from entities.paddle import Paddle
from entities.ball import Ball
from systems.renderer import GameRenderer
from systems.input_handler import InputHandler
from systems.ai import AIPlayer
from systems.particle_system import ParticleSystem
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
        
        # Show controller status
        if self.input_handler.controller_connected:
            print(f"Game ready with controller: {self.input_handler.controller.get_name()}")
        else:
            print("Game ready with keyboard input")

        # Initialize game entities
        self.init_paddles()
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Initialize AI players (players 1, 2, 3 are AI by default)
        self.ai_players = [
            AIPlayer(self.paddles[1], difficulty=0.7),  # Player 2 (right)
            AIPlayer(self.paddles[2], difficulty=0.6),  # Player 3 (top)
            AIPlayer(self.paddles[3], difficulty=0.6),  # Player 4 (bottom)
        ]

        # Game state - lives system
        self.lives = [5, 5, 5, 5]  # Each player starts with 5 lives
        self.alive_players = [True, True, True, True]  # Track which players are still alive
        self.starting_lives = 5
        
        # Game state management
        self.game_state = GAME_STATE_PLAYING
        self.previous_game_state = GAME_STATE_PLAYING  # Store state before pause
        self.aiming_player = -1  # Which player is currently aiming (-1 = none)
        self.aiming_timer = 0    # Timer for aiming phase
        self.aiming_angle = 0    # Current aiming angle
        
        # Pause input handling
        self.pause_key_pressed = False  # Track pause key state for single-press detection
        
        # Pause menu state
        self.pause_menu_selected = PAUSE_MENU_RESUME  # Currently selected menu option
        self.menu_nav_pressed = False  # Track menu navigation input for single-press detection
        self.menu_confirm_pressed = False  # Track confirmation input for single-press detection
        self.menu_cancel_pressed = False  # Track cancel input for single-press detection
        
        # AI aiming animation
        self.ai_target_angle = 0  # Target angle for AI
        self.ai_angle_speed = 1.5  # Degrees per frame for smooth movement

    def init_paddles(self):
        """Initialize the four paddles"""
        self.paddles = []

        # Player 1 - Left paddle (human player)
        left_paddle = Paddle(PADDLE_MARGIN, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                             0, 'vertical')
        self.paddles.append(left_paddle)

        # Player 2 - Right paddle (AI)
        right_paddle = Paddle(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
                              SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, 1, 'vertical')
        self.paddles.append(right_paddle)

        # Player 3 - Top paddle (AI)
        top_paddle = Paddle(SCREEN_WIDTH // 2 - H_PADDLE_WIDTH // 2, PADDLE_MARGIN,
                            2, 'horizontal')
        self.paddles.append(top_paddle)

        # Player 4 - Bottom paddle (AI)
        bottom_paddle = Paddle(SCREEN_WIDTH // 2 - H_PADDLE_WIDTH // 2,
                               SCREEN_HEIGHT - PADDLE_MARGIN - H_PADDLE_HEIGHT,
                               3, 'horizontal')
        self.paddles.append(bottom_paddle)

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
                if self.game_state != GAME_STATE_PAUSED:
                    self.toggle_pause()
                else:
                    # If already paused, quick resume with pause button
                    self.execute_menu_action(PAUSE_MENU_RESUME)
                self.pause_key_pressed = True
        else:
            self.pause_key_pressed = False
            
        # Handle pause menu navigation (only when paused)
        if self.game_state == GAME_STATE_PAUSED:
            self.handle_pause_menu_input()

    def handle_pause_menu_input(self):
        """Handle input for pause menu navigation"""
        # Check for menu navigation (up/down)
        nav_direction = self.input_handler.get_menu_navigation()
        if nav_direction != 0:
            if not self.menu_nav_pressed:  # Only trigger on initial press
                self.pause_menu_selected = (self.pause_menu_selected + nav_direction) % len(PAUSE_MENU_OPTIONS)
                self.menu_nav_pressed = True
        else:
            self.menu_nav_pressed = False
            
        # Check for confirmation input
        if self.input_handler.is_menu_confirm_pressed():
            if not self.menu_confirm_pressed:  # Only trigger on initial press
                self.execute_menu_action(self.pause_menu_selected)
                self.menu_confirm_pressed = True
        else:
            self.menu_confirm_pressed = False
            
        # Check for cancel input (B button or ESC)
        if self.input_handler.is_menu_cancel_pressed():
            if not self.menu_cancel_pressed:  # Only trigger on initial press
                # B button or ESC cancels pause menu (same as Resume)
                self.execute_menu_action(PAUSE_MENU_RESUME)
                self.menu_cancel_pressed = True
        else:
            self.menu_cancel_pressed = False

    def execute_menu_action(self, action):
        """Execute the selected menu action"""
        if action == PAUSE_MENU_RESUME:
            # Resume game
            self.game_state = self.previous_game_state
            print("Game resumed")
        elif action == PAUSE_MENU_RESTART:
            # Restart game
            self.reset_game()
            print("Game restarted")
        elif action == PAUSE_MENU_QUIT:
            # Quit game
            self.running = False
            print("Quitting game")

    def toggle_pause(self):
        """Toggle pause state"""
        if self.game_state == GAME_STATE_PAUSED:
            # Unpause - return to previous state
            self.game_state = self.previous_game_state
            print("Game resumed")
        else:
            # Pause - store current state and switch to paused
            self.previous_game_state = self.game_state
            self.game_state = GAME_STATE_PAUSED
            self.pause_menu_selected = PAUSE_MENU_RESUME  # Reset menu selection
            print("Game paused")

    def update(self):
        """Update game state based on current mode"""
        if self.game_state == GAME_STATE_PLAYING:
            self.update_playing_mode()
        elif self.game_state == GAME_STATE_AIMING:
            self.update_aiming_mode()
        elif self.game_state == GAME_STATE_PAUSED:
            # Don't update game logic when paused, only particle system
            pass
        
        # Always update particle system
        self.particle_system.update()
    
    def update_playing_mode(self):
        """Update game during normal play"""
        # Update input for human player (player 0)
        self.input_handler.update_paddle_movement([self.paddles[0]])

        # Update AI players (only for alive players)
        for i, ai_player in enumerate(self.ai_players):
            # AI players are at indices 1, 2, 3 (not 0 since player 0 is human)
            ai_player_index = i + 1
            if self.alive_players[ai_player_index]:
                ai_player.update(self.ball)

        # Update paddles (only for alive players)
        for i, paddle in enumerate(self.paddles):
            if self.alive_players[i]:
                paddle.update()

        # Update ball
        self.ball.update()

        # Check ball-paddle collisions (only with alive players)
        for i, paddle in enumerate(self.paddles):
            if self.alive_players[i] and self.ball.rect.colliderect(paddle.rect):
                self.ball.bounce_off_paddle(paddle)
                # Add particle effect for paddle hit
                self.particle_system.add_ball_impact_burst(self.ball.x, self.ball.y, paddle.color)
                # Add screen shake for paddle hit
                self.renderer.add_screen_shake(3, 8)
                break

        # Check for lives loss when ball hits edges
        self.check_lives_loss()
    
    def update_aiming_mode(self):
        """Update game during aiming phase"""
        # Update aiming timer
        self.aiming_timer -= 1
        
        # Update input for aiming player only
        if self.aiming_player >= 0 and self.alive_players[self.aiming_player]:
            if self.aiming_player == 0:  # Human player
                self.input_handler.update_paddle_movement([self.paddles[0]])
                # Actually update the paddle position
                self.paddles[0].update()
                self.update_aiming_angle()
            else:  # AI player - auto aim
                self.auto_aim_for_ai()
        
        # Launch ball when timer expires
        if self.aiming_timer <= 0:
            self.launch_ball()
    
    def update_aiming_angle(self):
        """Update aiming angle based on paddle position"""
        if self.aiming_player < 0:
            return
            
        paddle = self.paddles[self.aiming_player]
        paddle_center = paddle.get_center()
        
        # Convert paddle position to angle based on which player is aiming
        if self.aiming_player == 0:  # Left player
            # Paddle Y position controls angle from straight right
            normalized_pos = (paddle_center[1] - SCREEN_HEIGHT // 2) / (SCREEN_HEIGHT // 2)
            # Clamp normalized position to avoid extreme angles
            normalized_pos = max(-1, min(1, normalized_pos))
            self.aiming_angle = -normalized_pos * AIMING_ANGLE_RANGE  # Negative for upward
            
        elif self.aiming_player == 1:  # Right player  
            normalized_pos = (paddle_center[1] - SCREEN_HEIGHT // 2) / (SCREEN_HEIGHT // 2)
            normalized_pos = max(-1, min(1, normalized_pos))
            self.aiming_angle = 180 + normalized_pos * AIMING_ANGLE_RANGE
            
        elif self.aiming_player == 2:  # Top player
            normalized_pos = (paddle_center[0] - SCREEN_WIDTH // 2) / (SCREEN_WIDTH // 2)
            normalized_pos = max(-1, min(1, normalized_pos))
            self.aiming_angle = 90 + normalized_pos * AIMING_ANGLE_RANGE
            
        elif self.aiming_player == 3:  # Bottom player
            normalized_pos = (paddle_center[0] - SCREEN_WIDTH // 2) / (SCREEN_WIDTH // 2)
            normalized_pos = max(-1, min(1, normalized_pos))
            self.aiming_angle = 270 - normalized_pos * AIMING_ANGLE_RANGE
        
    
    def auto_aim_for_ai(self):
        """AI automatically aims with smooth animation"""
        import random
        
        # Set target angle once when AI starts aiming
        if not hasattr(self, 'ai_aiming_started') or not self.ai_aiming_started:
            base_angles = [0, 180, 90, 270]  # Straight out for each player
            base_angle = base_angles[self.aiming_player]
            # Larger range for more interesting AI behavior
            angle_offset = random.uniform(-45, 45)
            self.ai_target_angle = base_angle + angle_offset
            self.ai_aiming_started = True
            # AI has set target angle
        
        # Smoothly move current angle toward target
        angle_diff = self.ai_target_angle - self.aiming_angle
        
        # Handle angle wrapping (e.g., 350° to 10°)
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        
        # Move toward target smoothly
        if abs(angle_diff) > self.ai_angle_speed:
            move_direction = 1 if angle_diff > 0 else -1
            self.aiming_angle += self.ai_angle_speed * move_direction
        else:
            self.aiming_angle = self.ai_target_angle
        
        # Keep angle in valid range
        self.aiming_angle = self.aiming_angle % 360
    
    def launch_ball(self):
        """Launch the ball with the current aiming angle"""
        import math
        
        # Convert angle to velocity
        angle_rad = math.radians(self.aiming_angle)
        speed = BALL_SPEED
        
        self.ball.velocity.x = math.cos(angle_rad) * speed
        self.ball.velocity.y = math.sin(angle_rad) * speed
        
        # Ensure minimum speeds
        if abs(self.ball.velocity.x) < 2:
            self.ball.velocity.x = 2 if self.ball.velocity.x >= 0 else -2
        if abs(self.ball.velocity.y) < 2:
            self.ball.velocity.y = 2 if self.ball.velocity.y >= 0 else -2
        
        # Return to playing mode
        self.game_state = GAME_STATE_PLAYING
        self.aiming_player = -1
        self.aiming_timer = 0
        
        # Reset AI aiming state
        self.ai_aiming_started = False
    
    def enter_aiming_mode(self, losing_player):
        """Enter aiming mode for the specified player"""
        if self.alive_players[losing_player]:
            self.game_state = GAME_STATE_AIMING
            self.aiming_player = losing_player
            self.aiming_timer = AIMING_TIME
            
            # Reset AI aiming state
            self.ai_aiming_started = False
            self.ai_target_angle = 0
            
            # Position ball closer to losing player's side
            margin = 120  # Distance from boundary
            if losing_player == 0:  # Left player
                self.ball.x = BOUNDARY_THICKNESS + margin
                self.ball.y = SCREEN_HEIGHT // 2
                self.aiming_angle = 0  # Start aiming straight right
            elif losing_player == 1:  # Right player
                self.ball.x = SCREEN_WIDTH - BOUNDARY_THICKNESS - margin
                self.ball.y = SCREEN_HEIGHT // 2
                self.aiming_angle = 180  # Start aiming straight left
            elif losing_player == 2:  # Top player
                self.ball.x = SCREEN_WIDTH // 2
                self.ball.y = BOUNDARY_THICKNESS + margin
                self.aiming_angle = 90  # Start aiming straight down
            elif losing_player == 3:  # Bottom player
                self.ball.x = SCREEN_WIDTH // 2
                self.ball.y = SCREEN_HEIGHT - BOUNDARY_THICKNESS - margin
                self.aiming_angle = 270  # Start aiming straight up
            
            self.ball.velocity.x = 0
            self.ball.velocity.y = 0
        else:
            # Dead player - just reset ball normally
            self.ball.reset_position()

    def check_lives_loss(self):
        """Check ball boundary collisions - bounce off dead players, life loss for live players"""
        lost_life = False
        dying_player = -1
        bounced = False

        # Check left boundary
        if self.ball.x <= BOUNDARY_THICKNESS:
            if self.alive_players[0]:  # Live player - loses life
                self.lives[0] -= 1
                dying_player = 0
                lost_life = True
            else:  # Dead player - ball bounces
                self.ball.bounce_off_wall("left")
                self.particle_system.add_wall_impact_sparks(self.ball.x, self.ball.y)
                self.renderer.add_screen_shake(1, 4)
                bounced = True

        # Check right boundary
        elif self.ball.x >= SCREEN_WIDTH - BOUNDARY_THICKNESS:
            if self.alive_players[1]:  # Live player - loses life
                self.lives[1] -= 1
                dying_player = 1
                lost_life = True
            else:  # Dead player - ball bounces
                self.ball.bounce_off_wall("right")
                self.particle_system.add_wall_impact_sparks(self.ball.x, self.ball.y)
                self.renderer.add_screen_shake(1, 4)
                bounced = True

        # Check top boundary
        elif self.ball.y <= BOUNDARY_THICKNESS:
            if self.alive_players[2]:  # Live player - loses life
                self.lives[2] -= 1
                dying_player = 2
                lost_life = True
            else:  # Dead player - ball bounces
                self.ball.bounce_off_wall("top")
                self.particle_system.add_wall_impact_sparks(self.ball.x, self.ball.y)
                self.renderer.add_screen_shake(1, 4)
                bounced = True

        # Check bottom boundary
        elif self.ball.y >= SCREEN_HEIGHT - BOUNDARY_THICKNESS:
            if self.alive_players[3]:  # Live player - loses life
                self.lives[3] -= 1
                dying_player = 3
                lost_life = True
            else:  # Dead player - ball bounces
                self.ball.bounce_off_wall("bottom")
                self.particle_system.add_wall_impact_sparks(self.ball.x, self.ball.y)
                self.renderer.add_screen_shake(1, 4)
                bounced = True

        # Handle life loss
        if lost_life and dying_player >= 0:
            # Check if player is eliminated
            if self.lives[dying_player] <= 0:
                self.alive_players[dying_player] = False
                print(f"Player {dying_player + 1} eliminated!")
                
                # Add dramatic elimination particle effect
                self.particle_system.add_elimination_effect(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_COLORS[dying_player])
                
                # Strong screen shake for elimination
                self.renderer.add_screen_shake(10, 20)
                
                # Just reset ball for eliminated player
                self.ball.reset_position()
            else:
                # Player lost life but is still alive - enter aiming mode
                # Player lost a life but is still alive - enter aiming mode
                self.renderer.add_screen_shake(6, 15)
                self.enter_aiming_mode(dying_player)

            # Check for game over (only one player left)
            alive_count = sum(self.alive_players)
            if alive_count <= 1:
                self.game_over()

    def game_over(self):
        """Handle game over state"""
        # Find the last surviving player
        winner = -1
        for i, alive in enumerate(self.alive_players):
            if alive:
                winner = i
                break
        
        if winner >= 0:
            print(f"Player {winner + 1} wins! Last player standing with {self.lives[winner]} lives remaining!")
            # Add victory celebration
            self.particle_system.add_victory_celebration(
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_COLORS[winner])
        else:
            print("Game over - all players eliminated!")
        
        # Reset the game after a brief moment
        self.reset_game()

    def reset_game(self):
        """Reset the game to initial state"""
        self.lives = [5, 5, 5, 5]
        self.alive_players = [True, True, True, True]
        self.ball.reset_position()
        self.particle_system.clear()
        
        # Reset game state
        self.game_state = GAME_STATE_PLAYING
        self.previous_game_state = GAME_STATE_PLAYING
        self.aiming_player = -1
        self.aiming_timer = 0
        self.aiming_angle = 0
        self.ai_aiming_started = False
        self.pause_key_pressed = False
        self.pause_menu_selected = PAUSE_MENU_RESUME
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        self.menu_cancel_pressed = False

        # Reset paddle positions
        self.init_paddles()

        # Reinitialize AI with the new paddles
        self.ai_players = [
            AIPlayer(self.paddles[1], difficulty=0.7),  # Player 2 (right)
            AIPlayer(self.paddles[2], difficulty=0.6),  # Player 3 (top)
            AIPlayer(self.paddles[3], difficulty=0.6),  # Player 4 (bottom)
        ]

    def render(self):
        """Render the game"""
        self.renderer.render_frame(self.paddles, self.ball, self.lives, self.alive_players, 
                                 self.particle_system, self.game_state, self.aiming_player, 
                                 self.aiming_angle, self.aiming_timer, self.pause_menu_selected)
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()