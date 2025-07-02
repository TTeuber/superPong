import pygame
import random
from utils.constants import *


class EffectsRenderer:
    def __init__(self):
        # Screen shake effects
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

    def add_screen_shake(self, intensity, duration):
        """Add screen shake effect"""
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_duration = max(self.shake_duration, duration)
    
    def update_screen_shake(self):
        """Update screen shake offset"""
        if self.shake_duration > 0:
            # Calculate shake offset based on intensity
            max_offset = self.shake_intensity
            self.shake_offset_x = random.randint(-max_offset, max_offset)
            self.shake_offset_y = random.randint(-max_offset, max_offset)
            
            # Decrease shake over time
            self.shake_duration -= 1
            if self.shake_duration <= 0:
                self.shake_intensity = 0
                self.shake_offset_x = 0
                self.shake_offset_y = 0
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0

    def get_shake_offset(self):
        """Get current shake offset for rendering"""
        return (self.shake_offset_x, self.shake_offset_y)

    def apply_shake_to_surface(self, main_screen, game_surface):
        """Apply screen shake effect to a surface"""
        main_screen.fill(BLACK)  # Clear the main screen
        main_screen.blit(game_surface, (self.shake_offset_x, self.shake_offset_y))

    def create_glow_surface(self, width, height, color, alpha, position=(0, 0)):
        """Create a glow surface with specified parameters"""
        glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        glow_color = (*color, alpha)
        if width == height:  # Circular glow
            pygame.draw.circle(glow_surface, glow_color, (width // 2, height // 2), width // 2)
        else:  # Rectangular glow
            pygame.draw.rect(glow_surface, glow_color, (0, 0, width, height))
        return glow_surface

    def draw_multi_layer_glow(self, screen, rect, color, intensity=1.0, num_layers=3):
        """Draw multi-layer glow effect around a rectangle"""
        base_glow_size = int(15 * intensity)
        base_alpha = int(120 * intensity)
        
        for i in range(num_layers):
            layer_size = base_glow_size - (i * 3)
            layer_alpha = base_alpha // (i + 1)
            
            if layer_size > 0 and layer_alpha > 0:
                glow_surface = self.create_glow_surface(
                    rect.width + layer_size * 2, 
                    rect.height + layer_size * 2, 
                    color, 
                    layer_alpha
                )
                screen.blit(glow_surface, (rect.x - layer_size, rect.y - layer_size))

    def draw_circular_glow(self, screen, center, radius, color, intensity=1.0):
        """Draw circular glow effect"""
        glow_radius = int(radius * 2 * intensity)
        glow_alpha = int(100 * intensity)
        
        if glow_radius > 0 and glow_alpha > 0:
            glow_surface = self.create_glow_surface(
                glow_radius * 2, 
                glow_radius * 2, 
                color, 
                glow_alpha
            )
            screen.blit(glow_surface, (center[0] - glow_radius, center[1] - glow_radius))

    def create_trail_segment(self, position, size, color, alpha):
        """Create a single trail segment surface"""
        if alpha <= 0:
            return None
            
        trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        
        # Add glow to trail segments
        glow_alpha = alpha // 3
        if glow_alpha > 0:
            glow_color = (*color, glow_alpha)
            pygame.draw.circle(trail_surface, glow_color, (size, size), size)
        
        # Main trail segment
        trail_color = (*color, alpha)
        pygame.draw.circle(trail_surface, trail_color, (size, size), size // 2)
        
        return trail_surface

    def draw_enhanced_trail(self, screen, trail_positions, base_size, color):
        """Draw an enhanced trail with glow effects"""
        if len(trail_positions) < 2:
            return

        for i, pos in enumerate(trail_positions):
            progress = i / len(trail_positions)
            alpha = int(255 * progress * 0.7)  # Increased trail visibility
            
            if alpha > 0:
                trail_size = int(base_size * (0.3 + progress * 0.7))  # Variable size trail
                trail_surface = self.create_trail_segment(pos, trail_size, color, alpha)
                
                if trail_surface:
                    screen.blit(trail_surface, (pos[0] - trail_size, pos[1] - trail_size))

    def create_impact_effect(self, screen, position, color, intensity=1.0, size=20):
        """Create visual impact effect at a position"""
        effect_size = int(size * intensity)
        effect_alpha = int(150 * intensity)
        
        # Create burst effect
        burst_surface = pygame.Surface((effect_size * 2, effect_size * 2), pygame.SRCALPHA)
        
        # Multiple circles for burst effect
        for i in range(3):
            circle_size = effect_size - (i * 5)
            circle_alpha = effect_alpha // (i + 1)
            
            if circle_size > 0 and circle_alpha > 0:
                circle_color = (*color, circle_alpha)
                pygame.draw.circle(burst_surface, circle_color, (effect_size, effect_size), circle_size)
        
        screen.blit(burst_surface, (position[0] - effect_size, position[1] - effect_size))

    def reset_effects(self):
        """Reset all effect states"""
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0