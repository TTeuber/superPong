import pygame
import math
from utils.constants import *


class UIEffects:
    def __init__(self):
        # Initialize fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Load retro font for start screen
        try:
            self.font_retro_super_massive = pygame.font.Font("assets/PressStart2P-Regular.ttf", 128)  # For split title
            self.font_retro_massive = pygame.font.Font("assets/PressStart2P-Regular.ttf", 96)  # For split title
            self.font_retro_huge = pygame.font.Font("assets/PressStart2P-Regular.ttf", 72)  # For main title
            self.font_retro_large = pygame.font.Font("assets/PressStart2P-Regular.ttf", 48)
            self.font_retro_large_menu = pygame.font.Font("assets/PressStart2P-Regular.ttf", 40)  # For menu options
            self.font_retro_medium = pygame.font.Font("assets/PressStart2P-Regular.ttf", 32)
            self.font_retro_small = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)
        except:
            # Fallback to default fonts if retro font fails to load
            self.font_retro_super_massive = pygame.font.Font(None, 128)
            self.font_retro_massive = pygame.font.Font(None, 96)
            self.font_retro_huge = pygame.font.Font(None, 72)
            self.font_retro_large = self.font_large
            self.font_retro_large_menu = pygame.font.Font(None, 40)
            self.font_retro_medium = pygame.font.Font(None, 32)
            self.font_retro_small = self.font_small

    def draw_background_grid(self, screen, frame_count):
        """Draw an animated neon grid background"""
        # Pulsing grid intensity
        pulse = (math.sin(frame_count * 0.05) + 1) * 0.5
        base_intensity = 50
        grid_intensity = int(base_intensity + pulse * 20)
        
        grid_color = (0, grid_intensity, grid_intensity)
        grid_spacing = 50
        
        # Moving grid offset for subtle animation
        offset = int(frame_count * 0.2) % grid_spacing

        # Vertical lines with movement
        for x in range(-offset, SCREEN_WIDTH + grid_spacing, grid_spacing):
            if 0 <= x <= SCREEN_WIDTH:
                pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)

        # Horizontal lines with movement
        for y in range(-offset, SCREEN_HEIGHT + grid_spacing, grid_spacing):
            if 0 <= y <= SCREEN_HEIGHT:
                pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)

        # Center lines with enhanced pulsing
        center_pulse = (math.sin(frame_count * 0.12) + 1) * 0.5
        center_intensity = int(100 + center_pulse * 50)
        center_color = (0, center_intensity, center_intensity)
        
        pygame.draw.line(screen, center_color,
                         (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, center_color,
                         (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
        
        # Grid intersection highlights
        for x in range(0, SCREEN_WIDTH, grid_spacing * 2):
            for y in range(0, SCREEN_HEIGHT, grid_spacing * 2):
                highlight_alpha = int(30 * pulse)
                if highlight_alpha > 0:
                    highlight_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                    highlight_color = (*NEON_BLUE, highlight_alpha)
                    pygame.draw.circle(highlight_surface, highlight_color, (3, 3), 3)
                    screen.blit(highlight_surface, (x - 3, y - 3))

    def create_glow_effect(self, screen, text, font, color, position, glow_size=15, glow_alpha=80, num_layers=3):
        """Create a multi-layer glow effect for text"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        
        # Draw glow layers
        for i in range(num_layers):
            glow_surface = pygame.Surface((text_rect.width + glow_size * 2, text_rect.height + glow_size * 2), pygame.SRCALPHA)
            glow_color = (*color, glow_alpha // (i + 1))
            glow_text = font.render(text, True, glow_color)
            glow_text_rect = glow_text.get_rect(center=(glow_surface.get_width() // 2, glow_surface.get_height() // 2))
            glow_surface.blit(glow_text, glow_text_rect)
            screen.blit(glow_surface, (text_rect.x - glow_size, text_rect.y - glow_size))
        
        # Draw main text
        screen.blit(text_surface, text_rect)
        return text_rect

    def create_pulsing_glow_effect(self, screen, text, font, color, position, frame_count, glow_size=15, base_alpha=80, pulse_speed=0.1):
        """Create a pulsing glow effect for text"""
        pulse = (math.sin(frame_count * pulse_speed) + 1) * 0.5
        glow_alpha = int(base_alpha + pulse * 40)
        
        return self.create_glow_effect(screen, text, font, color, position, glow_size, glow_alpha)

    def draw_menu_selection_indicator(self, screen, position, color=NEON_GREEN, size=20):
        """Draw a selection arrow indicator"""
        arrow_text = "►"
        arrow_surface = self.font_large.render(arrow_text, True, color)
        arrow_rect = arrow_surface.get_rect(center=position)
        screen.blit(arrow_surface, arrow_rect)

    def draw_setting_arrows(self, screen, left_pos, right_pos, color=NEON_YELLOW):
        """Draw left and right arrows for settings navigation"""
        # Left arrow
        left_arrow_points = [
            (left_pos[0] - 10, left_pos[1]),
            (left_pos[0], left_pos[1] - 8),
            (left_pos[0], left_pos[1] + 8)
        ]
        pygame.draw.polygon(screen, color, left_arrow_points)
        
        # Right arrow  
        right_arrow_points = [
            (right_pos[0] + 10, right_pos[1]),
            (right_pos[0], right_pos[1] - 8),
            (right_pos[0], right_pos[1] + 8)
        ]
        pygame.draw.polygon(screen, color, right_arrow_points)

    def create_instruction_text(self, screen, instructions, start_y, spacing=20, color=(150, 150, 150)):
        """Create and render instruction text at the bottom of screens"""
        for i, instruction in enumerate(instructions):
            text_surface = self.font_small.render(instruction, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * spacing))
            screen.blit(text_surface, text_rect)

    def create_overlay(self, size, alpha=180):
        """Create a semi-transparent overlay surface"""
        overlay = pygame.Surface(size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        return overlay