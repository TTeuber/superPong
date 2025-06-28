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

# Paddle margins from edges
PADDLE_MARGIN = 50

# Game states
GAME_STATE_PLAYING = "playing"
GAME_STATE_AIMING = "aiming"

# Aiming system
AIMING_TIME = 90  # 3 seconds at 60 FPS
AIMING_ANGLE_RANGE = 60  # ±60 degrees from straight out

# Controller settings
CONTROLLER_DEADZONE = 0.15  # Dead zone for analog sticks (0.0-1.0)
CONTROLLER_SENSITIVITY = 1.0  # Movement sensitivity multiplier

# Nintendo Switch Pro Controller button/axis mappings
# These are typical values - may vary based on OS and drivers
SWITCH_CONTROLLER_MAPPINGS = {
    'left_stick_y': 1,      # Left analog stick Y-axis (up/down)
    'left_stick_x': 0,      # Left analog stick X-axis (left/right) - not used for vertical paddle
    'dpad_up': 13,          # D-pad up button
    'dpad_down': 14,        # D-pad down button
    'dpad_left': 15,        # D-pad left button  
    'dpad_right': 16,       # D-pad right button
    'a_button': 0,          # A button
    'b_button': 1,          # B button
    'x_button': 2,          # X button
    'y_button': 3,          # Y button
}