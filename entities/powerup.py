import pygame
import random
import math
from utils.constants import *

class PowerUp:
    def __init__(self, x, y, powerup_type=None):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE
        self.active = True
        
        # Choose random type if not specified
        if powerup_type is None:
            self.type = random.choice([POWERUP_PADDLE_SIZE, POWERUP_BALL_SPEED, POWERUP_SHIELD])
        else:
            self.type = powerup_type
            
        # Create collision rect
        self.rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2,
                               self.size, self.size)
        
        # Visual effects
        self.glow_radius = self.size
        self.glow_pulse = 0
        self.rotation_angle = 0
        self.spawn_timer = 0  # For spawn animation
        self.warning_phase = True  # Start in warning phase
        self.warning_timer = POWERUP_WARNING_TIME
        
        # Movement
        self.movement_angle = random.uniform(0, 2 * math.pi)
        self.movement_speed = random.uniform(0.5, 1.5)  # Slow movement speed
        self.movement_timer = 0
        self.direction_change_interval = random.randint(120, 300)  # 2-5 seconds
        
        # Choose effect variant randomly
        if self.type == POWERUP_PADDLE_SIZE:
            self.variant = random.choice(["increase_self", "decrease_enemies"])
        elif self.type == POWERUP_BALL_SPEED:
            self.variant = random.choice(["slow", "fast"])
        else:  # POWERUP_SHIELD
            self.variant = "shield"
            
    def update(self):
        """Update power-up state and animations"""
        if self.warning_phase:
            self.warning_timer -= 1
            if self.warning_timer <= 0:
                self.warning_phase = False
                self.spawn_timer = 30  # Half second spawn animation
        else:
            # Spawn animation
            if self.spawn_timer > 0:
                self.spawn_timer -= 1
                
            # Rotation animation
            self.rotation_angle += 2
            if self.rotation_angle >= 360:
                self.rotation_angle = 0
                
            # Glow pulse effect
            self.glow_pulse += 0.1
            self.glow_radius = self.size + 10 * math.sin(self.glow_pulse)
            
            # Slow movement
            self.movement_timer += 1
            if self.movement_timer >= self.direction_change_interval:
                # Change direction occasionally
                self.movement_angle = random.uniform(0, 2 * math.pi)
                self.movement_speed = random.uniform(0.5, 1.5)
                self.movement_timer = 0
                self.direction_change_interval = random.randint(120, 300)
            
            # Apply movement
            old_x, old_y = self.x, self.y
            self.x += math.cos(self.movement_angle) * self.movement_speed
            self.y += math.sin(self.movement_angle) * self.movement_speed
            
            # Keep within bounds (with some margin from edges)
            margin = 100
            if self.x < margin or self.x > SCREEN_WIDTH - margin:
                self.movement_angle = math.pi - self.movement_angle  # Reflect horizontally
                self.x = old_x
            if self.y < margin or self.y > SCREEN_HEIGHT - margin:
                self.movement_angle = -self.movement_angle  # Reflect vertically
                self.y = old_y
            
            # Update collision rect
            self.rect.x = self.x - self.size//2
            self.rect.y = self.y - self.size//2
            
    def can_collect(self):
        """Check if power-up can be collected (not in warning phase)"""
        return not self.warning_phase and self.spawn_timer <= 0
        
    def collect(self, player_id):
        """Mark power-up as collected by a player"""
        self.active = False
        return {
            'type': self.type,
            'variant': self.variant,
            'player_id': player_id,
            'duration': self.get_duration()
        }
        
    def get_duration(self):
        """Get duration for this power-up type"""
        if self.type == POWERUP_PADDLE_SIZE:
            return POWERUP_DURATION_PADDLE_SIZE
        elif self.type == POWERUP_BALL_SPEED:
            return POWERUP_DURATION_BALL_SPEED
        elif self.type == POWERUP_SHIELD:
            return POWERUP_DURATION_SHIELD
        return 0
        
    def get_color(self):
        """Get color based on power-up type"""
        if self.warning_phase:
            # Flashing white during warning
            flash = int(self.warning_timer / 10) % 2
            return WHITE if flash else NEON_PURPLE
            
        # Different shades of purple for different types
        if self.type == POWERUP_PADDLE_SIZE:
            return NEON_PURPLE
        elif self.type == POWERUP_BALL_SPEED:
            return (255, 0, 200)  # Pinkish purple
        else:  # POWERUP_SHIELD
            return (150, 0, 255)  # Bluish purple
            
    def get_icon_points(self):
        """Get points for drawing simple icon based on type"""
        cx, cy = self.x, self.y
        
        if self.type == POWERUP_PADDLE_SIZE:
            # Double arrow icon (resize)
            return [
                [(cx - 10, cy), (cx - 5, cy - 5), (cx - 5, cy + 5)],  # Left arrow
                [(cx + 10, cy), (cx + 5, cy - 5), (cx + 5, cy + 5)]   # Right arrow
            ]
        elif self.type == POWERUP_BALL_SPEED:
            # Lightning bolt icon (speed)
            return [[
                (cx - 5, cy - 10), (cx + 2, cy - 2),
                (cx - 2, cy + 2), (cx + 5, cy + 10),
                (cx + 2, cy + 2), (cx - 2, cy - 2)
            ]]
        else:  # POWERUP_SHIELD
            # Shield icon
            return [[
                (cx - 8, cy - 8), (cx + 8, cy - 8),
                (cx + 8, cy + 2), (cx, cy + 10),
                (cx - 8, cy + 2)
            ]]