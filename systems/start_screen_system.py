from entities.ball import Ball
from entities.paddle import Paddle
from systems.ai import AIPlayer
from utils.constants import *

class StartScreenSystem:
    """Manages the start screen with AI demo and menu navigation"""
    
    def __init__(self):
        # Menu state
        self.start_menu_selected = START_MENU_PLAY
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        
        # Callback functions
        self.on_play = None
        self.on_settings = None
        
        # AI demo game state
        self.demo_ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.demo_paddles = []
        self.demo_ai_players = []
        self.demo_frame_count = 0
        
        # Initialize demo game
        self.init_demo_game()
        
    def set_callbacks(self, on_play=None, on_settings=None):
        """Set callback functions for menu actions"""
        self.on_play = on_play
        self.on_settings = on_settings
        
    def init_demo_game(self):
        """Initialize the AI demo game with two paddles"""
        self.demo_paddles = []
        self.demo_ai_players = []
        
        # Create two paddles for demo - left and right
        left_paddle = Paddle(PADDLE_MARGIN, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, 0, 'vertical')
        right_paddle = Paddle(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH, 
                             SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, 1, 'vertical')
        
        self.demo_paddles = [left_paddle, right_paddle]
        
        # Create AI players for both paddles
        self.demo_ai_players = [
            AIPlayer(left_paddle, difficulty=0.5),   # Left paddle AI
            AIPlayer(right_paddle, difficulty=0.5),  # Right paddle AI
        ]
        
        # Set initial ball velocity
        self.demo_ball.velocity.x = BALL_SPEED * 0.8
        self.demo_ball.velocity.y = BALL_SPEED * 0.3
        
    def get_selected_option(self):
        """Get the currently selected menu option"""
        return self.start_menu_selected
        
    def get_demo_game_state(self):
        """Get the current demo game state for rendering"""
        return {
            'ball': self.demo_ball,
            'paddles': self.demo_paddles,
            'frame_count': self.demo_frame_count
        }
        
    def handle_start_menu_input(self, input_handler):
        """Handle input for start menu navigation"""
        # Check for menu navigation (up/down)
        nav_direction = input_handler.get_menu_navigation()
        if nav_direction != 0:
            if not self.menu_nav_pressed:
                # Navigate menu
                self.start_menu_selected = (self.start_menu_selected + nav_direction) % len(START_MENU_OPTIONS)
                self.menu_nav_pressed = True
        else:
            self.menu_nav_pressed = False
            
        # Check for confirmation input
        if input_handler.is_menu_confirm_pressed():
            if not self.menu_confirm_pressed:
                self.execute_menu_action(self.start_menu_selected)
                self.menu_confirm_pressed = True
        else:
            self.menu_confirm_pressed = False
            
    def execute_menu_action(self, action):
        """Execute the selected menu action"""
        if action == START_MENU_PLAY:
            if self.on_play:
                self.on_play()
        elif action == START_MENU_SETTINGS:
            if self.on_settings:
                self.on_settings()
                
    def update_demo_game(self):
        """Update the AI demo game"""
        self.demo_frame_count += 1
        
        # Update AI players
        for ai_player in self.demo_ai_players:
            ai_player.update(self.demo_ball)
            
        # Update paddles
        for paddle in self.demo_paddles:
            paddle.update()
            
        # Update ball
        self.demo_ball.update()
        
        # Check ball-paddle collisions
        for paddle in self.demo_paddles:
            if self.demo_ball.rect.colliderect(paddle.rect):
                self.demo_ball.bounce_off_paddle(paddle)
                
        # Check boundary collisions and reset if needed
        self.check_demo_boundary_collisions()
        
    def check_demo_boundary_collisions(self):
        """Check boundary collisions for demo game"""
        reset_needed = False
        
        # Check left/right boundaries (reset ball)
        if (self.demo_ball.x <= BOUNDARY_THICKNESS or 
            self.demo_ball.x >= SCREEN_WIDTH - BOUNDARY_THICKNESS):
            reset_needed = True
            
        # Check top/bottom boundaries (bounce)
        if self.demo_ball.y <= BOUNDARY_THICKNESS:
            self.demo_ball.bounce_off_wall("top")
        elif self.demo_ball.y >= SCREEN_HEIGHT - BOUNDARY_THICKNESS:
            self.demo_ball.bounce_off_wall("bottom")
            
        # Reset ball if it went out of bounds
        if reset_needed:
            self.demo_ball.reset_position()
            # Vary the starting velocity for interesting gameplay
            import random
            speed_x = BALL_SPEED * random.choice([-0.8, 0.8])
            speed_y = BALL_SPEED * random.uniform(-0.5, 0.5)
            self.demo_ball.velocity.x = speed_x
            self.demo_ball.velocity.y = speed_y
            
    def reset(self):
        """Reset start screen system"""
        self.start_menu_selected = START_MENU_PLAY
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        self.demo_frame_count = 0
        self.init_demo_game()