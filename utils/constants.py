# Game constants and configuration
import pygame

# Screen dimensions
SCREEN_WIDTH = 850
SCREEN_HEIGHT = 850
FPS = 60

# Colors (Retro Neon Theme)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (255, 255, 0)
NEON_PURPLE = (191, 0, 255)
NEON_ORANGE = (255, 165, 0)

# Paddle settings
PADDLE_SPEED = 10
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

# Horizontal paddles (top/bottom)
H_PADDLE_WIDTH = 100
H_PADDLE_HEIGHT = 15

# Ball settings
BALL_SIZE = 15
BALL_SPEED = 8
BALL_SPEED_BOOST = 0.1  # Optional speed boost on paddle hits (0.0 = no boost, 0.1 = 10% boost)

# Game boundaries
BOUNDARY_THICKNESS = 10

# Player positions
PLAYER_COLORS = [NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_YELLOW]

# Game settings
STARTING_LIVES = 1  # Number of lives each player starts with

# Paddle margins from edges
PADDLE_MARGIN = 50

# Game states
GAME_STATE_START_SCREEN = "start_screen"
GAME_STATE_PLAYING = "playing"
GAME_STATE_AIMING = "aiming"
GAME_STATE_PAUSED = "paused"
GAME_STATE_GAME_OVER = "game_over"

# Aiming system
AIMING_TIME = 90  # 3 seconds at 60 FPS
AIMING_ANGLE_RANGE = 60  # ±60 degrees from straight out

# Pause menu
PAUSE_MENU_OPTIONS = ["Resume", "Restart", "Quit"]
PAUSE_MENU_RESUME = 0
PAUSE_MENU_RESTART = 1
PAUSE_MENU_QUIT = 2

# Start screen menu
START_MENU_OPTIONS = ["Play", "Settings"]
START_MENU_PLAY = 0
START_MENU_SETTINGS = 1

# Game over menu
GAME_OVER_MENU_OPTIONS = ["Restart", "Main Menu", "Quit"]
GAME_OVER_RESTART = 0
GAME_OVER_MAIN_MENU = 1
GAME_OVER_QUIT = 2

# Controller settings
CONTROLLER_DEADZONE = 0.15  # Dead zone for analog sticks (0.0-1.0)
CONTROLLER_SENSITIVITY = 1.0  # Movement sensitivity multiplier

# Nintendo Switch Pro Controller button/axis mappings
# These values are based on testing - use controller_button_tester.py to verify
SWITCH_CONTROLLER_MAPPINGS = {
    # Analog sticks
    'left_stick_x': 0,      # Left analog stick X-axis (left/right)
    'left_stick_y': 1,      # Left analog stick Y-axis (up/down)
    'right_stick_x': 2,     # Right analog stick X-axis (left/right)
    'right_stick_y': 3,     # Right analog stick Y-axis (up/down)
    
    # Face buttons (tested values)
    'a_button': 0,          # A button (confirm) - bottom face button
    'b_button': 1,          # B button (cancel) - right face button
    'x_button': 3,          # X button - left face button
    'y_button': 2,          # Y button - top face button
    
    # System buttons
    'start_button': 7,      # Start/Plus button (pause)
    'select_button': 6,     # Select/Minus button (alternate pause)
    
    # Shoulder buttons
    'l_button': 4,          # L shoulder button
    'r_button': 5,          # R shoulder button
    'zl_button': 10,        # ZL trigger button
    'zr_button': 11,        # ZR trigger button
    
    # D-pad (often mapped as hat, but some drivers use buttons)
    'dpad_up': 12,          # D-pad up button
    'dpad_down': 13,        # D-pad down button
    'dpad_left': 14,        # D-pad left button  
    'dpad_right': 15,       # D-pad right button
}