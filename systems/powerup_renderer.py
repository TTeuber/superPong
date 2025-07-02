import pygame
import math
from utils.constants import *

class PowerUpRenderer:
    """Handles rendering of power-ups and their visual effects"""
    
    def __init__(self):
        self.pulse_timer = 0
        
    def render_powerups(self, screen, powerups, effects_renderer):
        """Render all active power-ups"""
        self.pulse_timer += 0.1
        
        for i, powerup in enumerate(powerups):
            if powerup.warning_phase:
                self.render_warning(screen, powerup, effects_renderer, show_instruction=(i == 0))
            else:
                self.render_powerup(screen, powerup, effects_renderer)
                
    def render_warning(self, screen, powerup, effects_renderer, show_instruction=False):
        """Render warning indicator before power-up spawns"""
        # Flashing circle at spawn position
        flash = int(powerup.warning_timer / 10) % 2
        if flash:
            # Draw warning circle
            warning_color = (255, 255, 255, 100)
            warning_radius = 40 + 10 * math.sin(self.pulse_timer * 2)
            
            # Create transparent surface
            surf = pygame.Surface((int(warning_radius * 2), int(warning_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, warning_color, 
                             (int(warning_radius), int(warning_radius)), 
                             int(warning_radius), 3)
                             
            screen.blit(surf, (powerup.x - warning_radius, powerup.y - warning_radius))
            
            # Draw collection radius circle
            collection_surf = pygame.Surface((POWERUP_COLLECT_RADIUS * 2, POWERUP_COLLECT_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(collection_surf, (255, 255, 255, 50), 
                             (POWERUP_COLLECT_RADIUS, POWERUP_COLLECT_RADIUS), 
                             POWERUP_COLLECT_RADIUS, 2)
            screen.blit(collection_surf, (powerup.x - POWERUP_COLLECT_RADIUS, powerup.y - POWERUP_COLLECT_RADIUS))
            
            # Draw "!" symbol
            font_size = 24
            font = pygame.font.Font(None, font_size)
            text = font.render("!", True, WHITE)
            text_rect = text.get_rect(center=(powerup.x, powerup.y))
            screen.blit(text, text_rect)
            
            # Add instruction text
            if show_instruction:  # Only show for first power-up
                instruction_font = pygame.font.Font(None, 20)
                instruction = instruction_font.render("Hit ball into power-up!", True, (200, 200, 200))
                inst_rect = instruction.get_rect(center=(powerup.x, powerup.y + 40))
                screen.blit(instruction, inst_rect)
            
    def render_powerup(self, screen, powerup, effects_renderer):
        """Render an active power-up"""
        # Spawn animation
        if powerup.spawn_timer > 0:
            scale = 1.0 - (powerup.spawn_timer / 30.0) * 0.5
        else:
            scale = 1.0
            
        # Apply scale to size
        current_size = int(powerup.size * scale)
        
        # Glow effect
        glow_color = powerup.get_color()
        effects_renderer.draw_glow(screen, powerup.x, powerup.y, 
                                 glow_color, int(powerup.glow_radius * scale))
        
        # Main body - rotating square
        if current_size > 0:
            # Create surface for rotation
            surf = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
            
            # Draw rotating square
            center = current_size
            points = []
            for i in range(4):
                angle = powerup.rotation_angle * math.pi / 180 + i * math.pi / 2
                x = center + current_size * 0.7 * math.cos(angle)
                y = center + current_size * 0.7 * math.sin(angle)
                points.append((x, y))
                
            pygame.draw.polygon(surf, glow_color, points, 3)
            
            # Draw icon inside
            icon_points = powerup.get_icon_points()
            for icon_part in icon_points:
                # Transform icon points relative to surface center
                transformed_points = []
                for px, py in icon_part:
                    # Get offset from powerup center
                    ox = px - powerup.x
                    oy = py - powerup.y
                    # Apply to surface center
                    transformed_points.append((center + ox * scale, center + oy * scale))
                    
                if len(transformed_points) > 2:
                    pygame.draw.polygon(surf, WHITE, transformed_points, 2)
                else:
                    pygame.draw.lines(surf, WHITE, False, transformed_points, 2)
                    
            # Blit to screen
            screen.blit(surf, (powerup.x - center, powerup.y - center))
            
    def render_active_effects(self, screen, paddles, active_effects, effects_renderer):
        """Render visual indicators for active power-up effects"""
        for effect in active_effects:
            if effect['duration'] <= 0:
                continue
                
            player_id = effect['player_id']
            if player_id < len(paddles):
                paddle = paddles[player_id]
                
                if effect['type'] == POWERUP_PADDLE_SIZE:
                    # Size effect - pulsing border
                    color = NEON_PURPLE
                    alpha = 100 + 50 * math.sin(self.pulse_timer * 3)
                    effects_renderer.draw_paddle_effect(screen, paddle, color, alpha)
                    
                elif effect['type'] == POWERUP_SHIELD:
                    # Shield effect - protective barrier
                    self.render_shield(screen, paddle, effects_renderer)
                    
        # Ball speed indicator
        for effect in active_effects:
            if effect['type'] == POWERUP_BALL_SPEED and effect['duration'] > 0:
                self.render_speed_indicator(screen, effect['variant'])
                break
                
    def render_shield(self, screen, paddle, effects_renderer):
        """Render shield effect around paddle"""
        # Create shield surface
        shield_color = (150, 0, 255, 100)
        
        if paddle.orientation == 'vertical':
            shield_width = paddle.width + 20
            shield_height = paddle.height + 10
        else:
            shield_width = paddle.width + 10
            shield_height = paddle.height + 20
            
        shield_surf = pygame.Surface((shield_width, shield_height), pygame.SRCALPHA)
        
        # Draw shield shape
        pygame.draw.rect(shield_surf, shield_color, shield_surf.get_rect(), 
                        border_radius=5)
        pygame.draw.rect(shield_surf, (255, 255, 255, 50), shield_surf.get_rect(), 
                        width=2, border_radius=5)
                        
        # Position shield
        shield_x = paddle.x - (shield_width - paddle.width) // 2
        shield_y = paddle.y - (shield_height - paddle.height) // 2
        
        screen.blit(shield_surf, (shield_x, shield_y))
        
    def render_speed_indicator(self, screen, variant):
        """Render ball speed indicator"""
        # Position in top-right corner
        x = SCREEN_WIDTH - 100
        y = 20
        
        # Draw speed icon
        if variant == "slow":
            color = (100, 100, 255)
            text = "SLOW"
        else:
            color = (255, 100, 100)
            text = "FAST"
            
        font = pygame.font.Font(None, 24)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        
        # Background
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect, border_radius=5)
        pygame.draw.rect(screen, color, bg_rect, width=2, border_radius=5)
        
        screen.blit(text_surf, text_rect)
        
    def render_collection_effect(self, particle_system, x, y, powerup_type):
        """Create particle effect when power-up is collected"""
        # Add burst of particles
        color = NEON_PURPLE
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            speed = 5
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle_system.add_particle(x, y, vx, vy, color, 30)