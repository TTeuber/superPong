import pygame
from utils.constants import *
from utils.math_utils import clamp

class Paddle:
    def __init__(self, x, y, player_id, orientation='vertical'):
        self.player_id = player_id
        self.orientation = orientation  # 'vertical' or 'horizontal'
        self.color = PLAYER_COLORS[player_id]

        # Set dimensions based on orientation
        if orientation == 'vertical':
            self.base_width = PADDLE_WIDTH
            self.base_height = PADDLE_HEIGHT
        else:  # horizontal
            self.base_width = H_PADDLE_WIDTH
            self.base_height = H_PADDLE_HEIGHT
            
        # Current dimensions (can be modified by power-ups)
        self.width = self.base_width
        self.height = self.base_height
        self.size_modifier = 1.0

        self.x = x
        self.y = y
        self.speed = PADDLE_SPEED

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

        # Create pygame rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Update paddle position based on movement flags"""
        if self.orientation == 'vertical':
            # Vertical paddles move up/down
            if self.moving_up:
                self.y -= self.speed
            if self.moving_down:
                self.y += self.speed

            # Clamp to screen boundaries
            self.y = clamp(self.y, BOUNDARY_THICKNESS,
                           SCREEN_HEIGHT - BOUNDARY_THICKNESS - self.height)

        else:  # horizontal
            # Horizontal paddles move left/right
            if self.moving_left:
                self.x -= self.speed
            if self.moving_right:
                self.x += self.speed

            # Clamp to screen boundaries
            self.x = clamp(self.x, BOUNDARY_THICKNESS,
                           SCREEN_WIDTH - BOUNDARY_THICKNESS - self.width)

        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y

    def get_center(self):
        """Get the center point of the paddle"""
        return (self.x + self.width // 2, self.y + self.height // 2)

    def set_movement(self, direction, active):
        """Set movement direction"""
        if direction == 'up':
            self.moving_up = active
        elif direction == 'down':
            self.moving_down = active
        elif direction == 'left':
            self.moving_left = active
        elif direction == 'right':
            self.moving_right = active
            
    def apply_size_modifier(self, modifier):
        """Apply a size modifier from power-ups"""
        self.size_modifier = modifier
        
        # Update dimensions based on modifier
        if self.orientation == 'vertical':
            self.height = int(self.base_height * modifier)
            # Keep width unchanged for vertical paddles
            self.width = self.base_width
        else:  # horizontal
            self.width = int(self.base_width * modifier)
            # Keep height unchanged for horizontal paddles
            self.height = self.base_height
            
        # Recenter paddle to avoid position jumps
        old_rect = self.rect.copy()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Adjust position to keep center point
        if self.orientation == 'vertical':
            self.y = old_rect.centery - self.height // 2
            self.y = clamp(self.y, BOUNDARY_THICKNESS,
                          SCREEN_HEIGHT - BOUNDARY_THICKNESS - self.height)
        else:
            self.x = old_rect.centerx - self.width // 2
            self.x = clamp(self.x, BOUNDARY_THICKNESS,
                          SCREEN_WIDTH - BOUNDARY_THICKNESS - self.width)
                          
        # Update rect with new position
        self.rect.x = self.x
        self.rect.y = self.y