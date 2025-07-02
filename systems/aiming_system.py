import math
import random
from utils.constants import *

class AimingSystem:
    """Manages aiming mode for both human and AI players"""
    
    def __init__(self):
        self.aiming_player = -1  # Which player is currently aiming (-1 = none)
        self.aiming_timer = 0    # Timer for aiming phase
        self.aiming_angle = 0    # Current aiming angle
        
        # AI aiming animation
        self.ai_target_angle = 0  # Target angle for AI
        self.ai_angle_speed = 1.5  # Degrees per frame for smooth movement
        self.ai_aiming_started = False
        
    def is_aiming_active(self):
        """Check if aiming mode is currently active"""
        return self.aiming_player >= 0
        
    def get_aiming_player(self):
        """Get the player currently aiming"""
        return self.aiming_player
        
    def get_aiming_angle(self):
        """Get the current aiming angle"""
        return self.aiming_angle
        
    def get_aiming_timer(self):
        """Get the remaining aiming timer"""
        return self.aiming_timer
        
    def enter_aiming_mode(self, losing_player, ball, alive_players):
        """Enter aiming mode for the specified player"""
        if alive_players[losing_player]:
            self.aiming_player = losing_player
            self.aiming_timer = AIMING_TIME
            
            # Reset AI aiming state
            self.ai_aiming_started = False
            self.ai_target_angle = 0
            
            # Position ball closer to losing player's side
            margin = 120  # Distance from boundary
            if losing_player == 0:  # Left player
                ball.x = BOUNDARY_THICKNESS + margin
                ball.y = SCREEN_HEIGHT // 2
                self.aiming_angle = 0  # Start aiming straight right
            elif losing_player == 1:  # Right player
                ball.x = SCREEN_WIDTH - BOUNDARY_THICKNESS - margin
                ball.y = SCREEN_HEIGHT // 2
                self.aiming_angle = 180  # Start aiming straight left
            elif losing_player == 2:  # Top player
                ball.x = SCREEN_WIDTH // 2
                ball.y = BOUNDARY_THICKNESS + margin
                self.aiming_angle = 90  # Start aiming straight down
            elif losing_player == 3:  # Bottom player
                ball.x = SCREEN_WIDTH // 2
                ball.y = SCREEN_HEIGHT - BOUNDARY_THICKNESS - margin
                self.aiming_angle = 270  # Start aiming straight up
            
            ball.velocity.x = 0
            ball.velocity.y = 0
        else:
            # Dead player - just reset ball normally
            ball.reset_position()
            
    def update_aiming_mode(self, paddles, alive_players, input_handler):
        """Update game during aiming phase"""
        # Update aiming timer
        self.aiming_timer -= 1
        
        # Update input for aiming player only
        if self.aiming_player >= 0 and alive_players[self.aiming_player]:
            if self.aiming_player == 0:  # Human player
                input_handler.update_paddle_movement([paddles[0]])
                # Actually update the paddle position
                paddles[0].update()
                self.update_aiming_angle(paddles[self.aiming_player])
            else:  # AI player - auto aim
                self.auto_aim_for_ai()
        
        # Return True if it's time to launch the ball
        return self.aiming_timer <= 0
        
    def update_aiming_angle(self, paddle):
        """Update aiming angle based on paddle position"""
        if self.aiming_player < 0:
            return
            
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
        # Set target angle once when AI starts aiming
        if not self.ai_aiming_started:
            base_angles = [0, 180, 90, 270]  # Straight out for each player
            base_angle = base_angles[self.aiming_player]
            # Larger range for more interesting AI behavior
            angle_offset = random.uniform(-45, 45)
            self.ai_target_angle = base_angle + angle_offset
            self.ai_aiming_started = True
        
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
        
    def launch_ball(self, ball):
        """Launch the ball with the current aiming angle"""
        # Convert angle to velocity
        angle_rad = math.radians(self.aiming_angle)
        speed = BALL_SPEED
        
        ball.velocity.x = math.cos(angle_rad) * speed
        ball.velocity.y = math.sin(angle_rad) * speed
        
        # Ensure minimum speeds
        if abs(ball.velocity.x) < 2:
            ball.velocity.x = 2 if ball.velocity.x >= 0 else -2
        if abs(ball.velocity.y) < 2:
            ball.velocity.y = 2 if ball.velocity.y >= 0 else -2
        
        # Set aiming player as the ball hitter for power-up collection
        ball.set_last_hitter(self.aiming_player)
        
        # Reset aiming state
        self.aiming_player = -1
        self.aiming_timer = 0
        self.ai_aiming_started = False
        
    def reset(self):
        """Reset aiming system to initial state"""
        self.aiming_player = -1
        self.aiming_timer = 0
        self.aiming_angle = 0
        self.ai_target_angle = 0
        self.ai_aiming_started = False