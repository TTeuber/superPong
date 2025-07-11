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
            self.type = random.choice(POWERUP_ALL_TYPES)
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
        elif self.type == POWERUP_SHIELD:
            self.variant = "shield"
        elif self.type == POWERUP_PADDLE_SWAP:
            self.variant = "swap"
        elif self.type == POWERUP_GHOST_BALL:
            self.variant = "ghost"
        elif self.type == POWERUP_MAGNETIZE:
            self.variant = "magnetize"
        elif self.type == POWERUP_DECOY_BALL:
            self.variant = "decoy"
        elif self.type == POWERUP_WILD_BOUNCE:
            self.variant = "wild"
        elif self.type == POWERUP_CONTROL_SCRAMBLE:
            self.variant = "scramble"
        else:
            self.variant = "default"
            
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
        elif self.type == POWERUP_PADDLE_SWAP:
            return POWERUP_DURATION_PADDLE_SWAP
        elif self.type == POWERUP_GHOST_BALL:
            return POWERUP_DURATION_GHOST_BALL
        elif self.type == POWERUP_MAGNETIZE:
            return POWERUP_DURATION_MAGNETIZE
        elif self.type == POWERUP_DECOY_BALL:
            return POWERUP_DURATION_DECOY_BALL
        elif self.type == POWERUP_WILD_BOUNCE:
            return POWERUP_DURATION_WILD_BOUNCE
        elif self.type == POWERUP_CONTROL_SCRAMBLE:
            return POWERUP_DURATION_CONTROL_SCRAMBLE
        return 0
        
    def get_color(self):
        """Get color based on power-up type"""
        if self.warning_phase:
            # Flashing white during warning
            flash = int(self.warning_timer / 10) % 2
            return WHITE if flash else self.get_base_color()
            
        return self.get_base_color()
    
    def get_base_color(self):
        """Get base color for power-up type"""
        # Classic power-ups (purple tones)
        if self.type == POWERUP_PADDLE_SIZE:
            return NEON_PURPLE
        elif self.type == POWERUP_BALL_SPEED:
            return (255, 0, 200)  # Pinkish purple
        elif self.type == POWERUP_SHIELD:
            return (150, 0, 255)  # Bluish purple
        # Strategic power-ups (different colors)
        elif self.type == POWERUP_PADDLE_SWAP:
            return NEON_ORANGE  # Orange for swap
        elif self.type == POWERUP_GHOST_BALL:
            return NEON_CYAN    # Cyan for ghost
        elif self.type == POWERUP_MAGNETIZE:
            return NEON_YELLOW  # Yellow for magnetize
        # Chaos power-ups (bright, chaotic colors)
        elif self.type == POWERUP_DECOY_BALL:
            return (255, 100, 255)  # Bright magenta for decoy
        elif self.type == POWERUP_WILD_BOUNCE:
            return (255, 50, 0)     # Bright red-orange for wild
        elif self.type == POWERUP_CONTROL_SCRAMBLE:
            return (100, 255, 100)  # Bright lime green for scramble
        else:
            return NEON_PURPLE  # Default
            
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
        elif self.type == POWERUP_SHIELD:
            # Shield icon
            return [[
                (cx - 8, cy - 8), (cx + 8, cy - 8),
                (cx + 8, cy + 2), (cx, cy + 10),
                (cx - 8, cy + 2)
            ]]
        elif self.type == POWERUP_PADDLE_SWAP:
            # Circular arrows (swap)
            return [
                [(cx - 8, cy - 4), (cx - 4, cy - 8), (cx, cy - 4)],  # Top arrow
                [(cx + 8, cy + 4), (cx + 4, cy + 8), (cx, cy + 4)]   # Bottom arrow
            ]
        elif self.type == POWERUP_GHOST_BALL:
            # Ghost shape (wavy bottom)
            return [[
                (cx - 8, cy - 6), (cx - 8, cy + 2),
                (cx - 6, cy + 6), (cx - 4, cy + 2),
                (cx - 2, cy + 6), (cx, cy + 2),
                (cx + 2, cy + 6), (cx + 4, cy + 2),
                (cx + 6, cy + 6), (cx + 8, cy + 2),
                (cx + 8, cy - 6), (cx + 4, cy - 10),
                (cx - 4, cy - 10)
            ]]
        elif self.type == POWERUP_MAGNETIZE:
            # Magnet shape (horseshoe)
            return [
                [(cx - 8, cy - 8), (cx - 8, cy + 6)],  # Left line
                [(cx + 8, cy - 8), (cx + 8, cy + 6)],  # Right line
                [(cx - 8, cy + 6), (cx - 4, cy + 6)],  # Left bottom
                [(cx + 8, cy + 6), (cx + 4, cy + 6)]   # Right bottom
            ]
        elif self.type == POWERUP_DECOY_BALL:
            # Two overlapping circles (real + fake ball)
            return [
                [(cx - 6, cy - 3), (cx - 3, cy - 6), (cx + 3, cy - 6), (cx + 6, cy - 3),
                 (cx + 6, cy + 3), (cx + 3, cy + 6), (cx - 3, cy + 6), (cx - 6, cy + 3)],  # Main circle
                [(cx - 2, cy + 1), (cx + 1, cy - 2), (cx + 5, cy - 2), (cx + 8, cy + 1),
                 (cx + 8, cy + 5), (cx + 5, cy + 8), (cx + 1, cy + 8), (cx - 2, cy + 5)]   # Offset circle
            ]
        elif self.type == POWERUP_WILD_BOUNCE:
            # Chaotic zigzag pattern
            return [[
                (cx - 8, cy - 6), (cx - 4, cy + 2), (cx, cy - 4),
                (cx + 4, cy + 6), (cx + 8, cy - 2), (cx + 6, cy + 4),
                (cx + 2, cy - 8), (cx - 2, cy + 8), (cx - 6, cy - 4)
            ]]
        elif self.type == POWERUP_CONTROL_SCRAMBLE:
            # Curved arrows in different directions (scrambled controls)
            return [
                [(cx - 8, cy - 4), (cx - 4, cy - 8), (cx, cy - 4), (cx - 2, cy - 6)],  # Top left arrow
                [(cx + 8, cy - 4), (cx + 4, cy - 8), (cx, cy - 4), (cx + 2, cy - 6)],  # Top right arrow
                [(cx - 4, cy + 8), (cx - 8, cy + 4), (cx - 4, cy), (cx - 6, cy + 2)],  # Bottom left arrow
                [(cx + 4, cy + 8), (cx + 8, cy + 4), (cx + 4, cy), (cx + 6, cy + 2)]   # Bottom right arrow
            ]
        else:
            # Default icon (question mark)
            return [[
                (cx - 4, cy - 8), (cx + 4, cy - 8),
                (cx + 4, cy - 4), (cx, cy),
                (cx, cy + 4), (cx, cy + 8)
            ]]