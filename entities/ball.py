import pygame
import random
import math
from utils.constants import *
from utils.math_utils import Vector2, clamp

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = BALL_SIZE
        self.speed = BALL_SPEED

        # Random starting direction
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = Vector2(
            math.cos(angle) * self.speed,
            math.sin(angle) * self.speed
        )

        # Ensure minimum speed in both directions to avoid getting stuck
        if abs(self.velocity.x) < 2:
            self.velocity.x = 2 if self.velocity.x >= 0 else -2
        if abs(self.velocity.y) < 2:
            self.velocity.y = 2 if self.velocity.y >= 0 else -2

        self.rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2,
                                self.size, self.size)

        # Visual effects
        self.trail_positions = []
        self.max_trail_length = 15
        self.last_hit_color = NEON_BLUE  # Color from last paddle hit
        self.glow_intensity = 1.0

    def update(self):
        """Update ball position and handle wall collisions"""
        # Store position for trail effect
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
        
        # Gradually reduce glow intensity
        if self.glow_intensity > 1.0:
            self.glow_intensity -= 0.02

        # Update position
        self.x += self.velocity.x
        self.y += self.velocity.y

        # Update collision rect
        self.rect.x = self.x - self.size//2
        self.rect.y = self.y - self.size//2

    def bounce_off_paddle(self, paddle):
        """Handle collision with paddle"""
        paddle_center = paddle.get_center()
        
        # Store the color of the paddle that hit the ball
        self.last_hit_color = paddle.color
        self.glow_intensity = 1.5  # Boost glow intensity on hit

        # Calculate relative hit position (-1 to 1)
        if paddle.orientation == 'vertical':
            relative_intersect_y = (self.y - paddle_center[1]) / (paddle.height / 2)
            relative_intersect_y = clamp(relative_intersect_y, -1, 1)

            # Reflect horizontally and add vertical spin based on hit position
            self.velocity.x = -self.velocity.x
            self.velocity.y = relative_intersect_y * self.speed * 0.7

            # Move ball away from paddle to prevent sticking
            if paddle.x < SCREEN_WIDTH // 2:  # Left paddle
                self.x = paddle.x + paddle.width + self.size//2 + 5
            else:  # Right paddle
                self.x = paddle.x - self.size//2 - 5

        else:  # horizontal paddle
            relative_intersect_x = (self.x - paddle_center[0]) / (paddle.width / 2)
            relative_intersect_x = clamp(relative_intersect_x, -1, 1)

            # Reflect vertically and add horizontal spin based on hit position
            self.velocity.y = -self.velocity.y
            self.velocity.x = relative_intersect_x * self.speed * 0.7

            # Move ball away from paddle to prevent sticking
            if paddle.y < SCREEN_HEIGHT // 2:  # Top paddle
                self.y = paddle.y + paddle.height + self.size//2 + 5
            else:  # Bottom paddle
                self.y = paddle.y - self.size//2 - 5

        # Apply optional speed boost on paddle hit
        target_speed = self.speed * (1.0 + BALL_SPEED_BOOST)
        
        # Normalize velocity to maintain constant speed
        self.normalize_velocity(target_speed)
        
        # Ensure minimum speed in each direction to prevent ball from getting stuck
        if abs(self.velocity.x) < 1:
            self.velocity.x = 1 if self.velocity.x >= 0 else -1
        if abs(self.velocity.y) < 1:
            self.velocity.y = 1 if self.velocity.y >= 0 else -1
            
        # Re-normalize after minimum speed adjustment
        self.normalize_velocity(target_speed)
    
    def bounce_off_wall(self, wall_side):
        """Bounce ball off a wall (for dead player boundaries)"""
        if wall_side == "left":
            self.x = BOUNDARY_THICKNESS + self.size//2
            self.velocity.x = abs(self.velocity.x)  # Ensure rightward velocity
        elif wall_side == "right":
            self.x = SCREEN_WIDTH - BOUNDARY_THICKNESS - self.size//2
            self.velocity.x = -abs(self.velocity.x)  # Ensure leftward velocity
        elif wall_side == "top":
            self.y = BOUNDARY_THICKNESS + self.size//2
            self.velocity.y = abs(self.velocity.y)  # Ensure downward velocity
        elif wall_side == "bottom":
            self.y = SCREEN_HEIGHT - BOUNDARY_THICKNESS - self.size//2
            self.velocity.y = -abs(self.velocity.y)  # Ensure upward velocity
        
        # Update collision rect
        self.rect.x = self.x - self.size//2
        self.rect.y = self.y - self.size//2

    def reset_position(self):
        """Reset ball to center with random direction"""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.trail_positions.clear()

        # Random starting direction
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = Vector2(
            math.cos(angle) * self.speed,
            math.sin(angle) * self.speed
        )
        
        # Reset visual effects
        self.last_hit_color = NEON_BLUE
        self.glow_intensity = 1.0

        # Ensure minimum speed in both directions
        if abs(self.velocity.x) < 2:
            self.velocity.x = 2 if self.velocity.x >= 0 else -2
        if abs(self.velocity.y) < 2:
            self.velocity.y = 2 if self.velocity.y >= 0 else -2

    def normalize_velocity(self, target_speed=None):
        """Normalize velocity to maintain constant speed"""
        if target_speed is None:
            target_speed = self.speed
        
        # Calculate current speed
        current_speed = math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
        
        if current_speed > 0:
            # Normalize to target speed
            scale_factor = target_speed / current_speed
            self.velocity.x *= scale_factor
            self.velocity.y *= scale_factor
        else:
            # If somehow velocity is zero, set a default direction
            self.velocity.x = target_speed
            self.velocity.y = 0