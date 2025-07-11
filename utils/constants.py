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
NEON_CYAN = (0, 255, 255)  # Same as NEON_BLUE for consistency
NEON_PINK = (255, 20, 147)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (255, 255, 0)
NEON_PURPLE = (191, 0, 255)
NEON_ORANGE = (255, 165, 0)

# Paddle settings
PADDLE_SPEED = 8
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
STARTING_LIVES = 3  # Number of lives each player starts with

# Paddle margins from edges
PADDLE_MARGIN = 50

# Game states
GAME_STATE_START_SCREEN = "start_screen"
GAME_STATE_SETTINGS = "settings"
GAME_STATE_PLAYING = "playing"
GAME_STATE_AIMING = "aiming"
GAME_STATE_PAUSED = "paused"
GAME_STATE_GAME_OVER = "game_over"

# Aiming system
AIMING_TIME = 90  # 3 seconds at 60 FPS
AIMING_ANGLE_RANGE = 60  # ±60 degrees from straight out

# Pause menu
PAUSE_MENU_OPTIONS = ["Resume", "Restart", "Main Menu", "Quit"]
PAUSE_MENU_RESUME = 0
PAUSE_MENU_RESTART = 1
PAUSE_MENU_MAIN_MENU = 2
PAUSE_MENU_QUIT = 3

# Start screen menu
START_MENU_OPTIONS = ["Play", "Settings"]
START_MENU_PLAY = 0
START_MENU_SETTINGS = 1

# Game over menu
GAME_OVER_MENU_OPTIONS = ["Restart", "Main Menu", "Quit"]
GAME_OVER_RESTART = 0
GAME_OVER_MAIN_MENU = 1
GAME_OVER_QUIT = 2

# Settings menu
SETTINGS_MENU_OPTIONS = ["Difficulty", "Sound", "Controller Sensitivity", "Power-ups", "Back"]
SETTINGS_MENU_DIFFICULTY = 0
SETTINGS_MENU_SOUND = 1
SETTINGS_MENU_CONTROLLER = 2
SETTINGS_MENU_POWERUPS = 3
SETTINGS_MENU_BACK = 4

# Difficulty levels
DIFFICULTY_EASY = "Easy"
DIFFICULTY_MEDIUM = "Medium"
DIFFICULTY_HARD = "Hard"
DIFFICULTY_VALUES = {
    DIFFICULTY_EASY: 0.1,    # Much easier - beginner friendly
    DIFFICULTY_MEDIUM: 0.3,  # Moderate challenge  
    DIFFICULTY_HARD: 0.6     # Challenging but fair
}
DIFFICULTY_OPTIONS = [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD]

# Controller settings
CONTROLLER_DEADZONE = 0.15  # Dead zone for analog sticks (0.0-1.0)
CONTROLLER_SENSITIVITY = 1.0  # Movement sensitivity multiplier

# AI Prediction settings
AI_PREDICTION_ENABLED = True           # Enable trajectory prediction
AI_PREDICTION_LOOKAHEAD_TIME = 60     # Frames to look ahead (1 second at 60fps)
AI_MAX_PREDICTION_BOUNCES = 1          # Maximum wall bounces to predict
AI_PREDICTION_ACCURACY = 0.9           # Base prediction accuracy (0.0-1.0)

# AI Strategic Positioning settings
AI_CENTER_SEEK_ENABLED = True          # Enable center-seeking behavior
AI_CENTER_SEEK_STRENGTH = 0.7          # How strongly AI seeks center (0.0-1.0)
AI_ANTICIPATION_DISTANCE = 250         # Distance threshold for anticipatory movement
AI_DEFENSIVE_ZONE_SIZE = 300           # Size of defensive zone around paddle center (increased)
AI_MIN_THREAT_DISTANCE = 400           # Minimum distance to consider ball a threat
AI_OPPOSITE_WALL_THRESHOLD = 0.8       # Velocity threshold for detecting opposite wall direction

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

# Power-up System Constants
POWERUP_SIZE = 40  # Size of power-up pickup
POWERUP_SPAWN_MIN_TIME = 600  # 20 seconds at 60 FPS
POWERUP_SPAWN_MAX_TIME = 900  # 30 seconds at 60 FPS
POWERUP_WARNING_TIME = 120     # 3 seconds warning before spawn
POWERUP_COLLECT_RADIUS = 50    # Collection radius for power-ups (ball-based)

# Power-up Types (Simplified)
POWERUP_PADDLE_SIZE = "paddle_size"
POWERUP_SHIELD = "shield"
POWERUP_DECOY_BALL = "decoy_ball"

# Power-up Selection System (Simplified)
POWERUP_ALL_TYPES = [POWERUP_PADDLE_SIZE, POWERUP_SHIELD, POWERUP_DECOY_BALL]

# Legacy power-up types (kept for compatibility)
POWERUP_BALL_SPEED = "ball_speed"
POWERUP_PADDLE_SWAP = "paddle_swap"
POWERUP_GHOST_BALL = "ghost_ball"
POWERUP_MAGNETIZE = "magnetize"
POWERUP_WILD_BOUNCE = "wild_bounce"
POWERUP_CONTROL_SCRAMBLE = "control_scramble"
POWERUP_CLASSIC_TYPES = [POWERUP_PADDLE_SIZE, POWERUP_SHIELD]
POWERUP_STRATEGIC_TYPES = []
POWERUP_CHAOS_TYPES = [POWERUP_DECOY_BALL]

# Power-up Categories for UI
POWERUP_CATEGORIES = {
    "Classic": POWERUP_CLASSIC_TYPES,
    "Strategic": POWERUP_STRATEGIC_TYPES,
    "Chaos": POWERUP_CHAOS_TYPES
}

# Power-up Descriptions
POWERUP_DESCRIPTIONS = {
    POWERUP_PADDLE_SIZE: "Increase your paddle size or decrease enemies'",
    POWERUP_SHIELD: "Protect from one life loss",
    POWERUP_DECOY_BALL: "Spawn a fake ball that doesn't cause life loss",
    # Legacy descriptions
    POWERUP_BALL_SPEED: "Speed up or slow down the ball",
    POWERUP_PADDLE_SWAP: "Swap positions with a random opponent",
    POWERUP_GHOST_BALL: "Ball passes through enemy paddles",
    POWERUP_MAGNETIZE: "Your paddle attracts the ball",
    POWERUP_WILD_BOUNCE: "Ball randomly changes direction during flight",
    POWERUP_CONTROL_SCRAMBLE: "All player controls get scrambled"
}

# Power-up Durations (in frames at 60 FPS)
POWERUP_DURATION_PADDLE_SIZE = 480    # 8 seconds
POWERUP_DURATION_BALL_SPEED = 600     # 10 seconds
POWERUP_DURATION_SHIELD = 600         # 10 seconds
POWERUP_DURATION_PADDLE_SWAP = -1     # Instant effect
POWERUP_DURATION_GHOST_BALL = 240     # 4 seconds
POWERUP_DURATION_MAGNETIZE = 480      # 8 seconds
POWERUP_DURATION_DECOY_BALL = 480     # 8 seconds
POWERUP_DURATION_WILD_BOUNCE = 600    # 10 seconds
POWERUP_DURATION_CONTROL_SCRAMBLE = 360  # 6 seconds

# Power-up Effect Values
POWERUP_PADDLE_SIZE_INCREASE = 1.5    # 50% larger
POWERUP_PADDLE_SIZE_DECREASE = 0.75   # 25% smaller for enemies
POWERUP_BALL_SPEED_SLOW = 0.75        # 75% speed
POWERUP_BALL_SPEED_FAST = 1.25        # 125% speed

# Strategic Power-up Effect Values
POWERUP_MAGNETIC_FIELD_RADIUS = 120   # Pixels from paddle center
POWERUP_MAGNETIC_FORCE = 0.3          # Attraction force strength

# Chaos Power-up Effect Values
POWERUP_WILD_BOUNCE_ANGLE_RANGE = 30  # ±30 degrees random deflection
POWERUP_WILD_BOUNCE_INTERVAL = 150    # Frames between direction changes (2.5 seconds)
POWERUP_WILD_BOUNCE_MIN_INTERVAL = 90  # Minimum interval (1.5 seconds)
POWERUP_DECOY_BALL_TRANSPARENCY = 0.9  # Slight transparency to hint it's fake

# Power-up Spawn Positions (center area variations)
POWERUP_SPAWN_POSITIONS = [
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),  # Center
    (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2),  # Left of center
    (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2),  # Right of center
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100),  # Above center
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),  # Below center
]