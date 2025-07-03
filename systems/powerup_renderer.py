import pygame
import math
import random
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
                    
                elif effect['type'] == POWERUP_MAGNETIZE:
                    # Magnetize effect - magnetic field
                    self.render_magnetic_field(screen, paddle, effects_renderer)
                    
        # Ball speed indicator
        for effect in active_effects:
            if effect['type'] == POWERUP_BALL_SPEED and effect['duration'] > 0:
                self.render_speed_indicator(screen, effect['variant'])
                break
                
        # Ghost ball indicator
        for effect in active_effects:
            if effect['type'] == POWERUP_GHOST_BALL and effect['duration'] > 0:
                self.render_ghost_ball_indicator(screen, effect['player_id'])
                break
                
        # Wild bounce indicator
        for effect in active_effects:
            if effect['type'] == POWERUP_WILD_BOUNCE and effect['duration'] > 0:
                self.render_wild_bounce_indicator(screen)
                break
                
        # Control scramble indicator
        for effect in active_effects:
            if effect['type'] == POWERUP_CONTROL_SCRAMBLE and effect['duration'] > 0:
                self.render_control_scramble_indicator(screen)
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
        
    def render_magnetic_field(self, screen, paddle, effects_renderer):
        """Render magnetic field effect around paddle"""
        # Create pulsing magnetic field visualization
        field_color = (255, 255, 0, 60)  # Yellow with transparency
        pulse_scale = 1.0 + 0.3 * math.sin(self.pulse_timer * 4)
        field_radius = int(POWERUP_MAGNETIC_FIELD_RADIUS * pulse_scale)
        
        paddle_center = paddle.get_center()
        
        # Create magnetic field surface
        field_surf = pygame.Surface((field_radius * 2, field_radius * 2), pygame.SRCALPHA)
        
        # Draw concentric circles for magnetic field
        for i in range(3):
            radius = field_radius - i * 20
            if radius > 0:
                alpha = 40 - i * 10
                circle_color = (255, 255, 0, alpha)
                pygame.draw.circle(field_surf, circle_color, (field_radius, field_radius), radius, 2)
        
        # Position and blit
        field_x = paddle_center[0] - field_radius
        field_y = paddle_center[1] - field_radius
        screen.blit(field_surf, (field_x, field_y))
        
    def render_ghost_ball_indicator(self, screen, player_id):
        """Render ghost ball effect indicator"""
        # Position in corner based on player
        if player_id == 0:  # Left player
            x, y = 20, SCREEN_HEIGHT // 2
        elif player_id == 1:  # Right player
            x, y = SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2
        elif player_id == 2:  # Top player
            x, y = SCREEN_WIDTH // 2, 20
        else:  # Bottom player
            x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20
            
        # Draw ghost icon
        color = (0, 255, 255, 150)  # Semi-transparent cyan
        font = pygame.font.Font(None, 24)
        text = font.render("GHOST", True, color)
        text_rect = text.get_rect(center=(x, y))
        
        # Background
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(screen, (0, 0, 0, 100), bg_rect, border_radius=5)
        pygame.draw.rect(screen, color, bg_rect, width=2, border_radius=5)
        
        screen.blit(text, text_rect)
        
    def render_wild_bounce_indicator(self, screen):
        """Render wild bounce effect indicator"""
        # Position in top-center
        x = SCREEN_WIDTH // 2
        y = 20
        
        # Chaotic color effect
        color = (255, 50, 0)  # Bright red-orange
        font = pygame.font.Font(None, 24)
        text = font.render("WILD BOUNCE", True, color)
        text_rect = text.get_rect(center=(x, y))
        
        # Background with chaotic border
        bg_rect = text_rect.inflate(25, 15)
        pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect, border_radius=5)
        pygame.draw.rect(screen, color, bg_rect, width=3, border_radius=5)
        
        # Add zigzag decoration
        zigzag_y = bg_rect.bottom + 5
        for i in range(5):
            start_x = bg_rect.left + i * 20
            end_x = start_x + 10
            zigzag_start_y = zigzag_y + (i % 2) * 5
            zigzag_end_y = zigzag_y + ((i + 1) % 2) * 5
            pygame.draw.line(screen, color, (start_x, zigzag_start_y), (end_x, zigzag_end_y), 2)
        
        screen.blit(text, text_rect)
        
    def render_control_scramble_indicator(self, screen):
        """Render control scramble effect indicator"""
        # Position in bottom-center
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT - 30
        
        # Scrambled color effect
        color = (100, 255, 100)  # Bright lime green
        font = pygame.font.Font(None, 24)
        text = font.render("CONTROLS SCRAMBLED", True, color)
        text_rect = text.get_rect(center=(x, y))
        
        # Background
        bg_rect = text_rect.inflate(30, 15)
        pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect, border_radius=5)
        pygame.draw.rect(screen, color, bg_rect, width=3, border_radius=5)
        
        # Add swirling decoration
        swirl_center_x = bg_rect.centerx
        swirl_center_y = bg_rect.top - 10
        for i in range(8):
            angle = (i / 8) * 2 * math.pi + self.pulse_timer
            radius = 8
            point_x = swirl_center_x + radius * math.cos(angle)
            point_y = swirl_center_y + radius * math.sin(angle)
            pygame.draw.circle(screen, color, (int(point_x), int(point_y)), 2)
        
        screen.blit(text, text_rect)
        
    def render_decoy_balls(self, screen, decoy_balls, effects_renderer):
        """Render all active decoy balls"""
        for decoy_ball in decoy_balls:
            self.render_decoy_ball(screen, decoy_ball, effects_renderer)
            
    def render_decoy_ball(self, screen, decoy_ball, effects_renderer):
        """Render a single decoy ball with transparency"""
        # Create transparent surface for decoy ball
        ball_surface = pygame.Surface((decoy_ball.size * 4, decoy_ball.size * 4), pygame.SRCALPHA)
        
        # Calculate center position on surface
        surf_center_x = decoy_ball.size * 2
        surf_center_y = decoy_ball.size * 2
        
        # Draw glow effect (dimmer than real ball)
        glow_color = (255, 100, 255)  # Magenta
        glow_alpha = decoy_ball.alpha // 3  # Much dimmer glow
        for i in range(3):
            glow_radius = decoy_ball.size + i * 5
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_alpha_layer = glow_alpha // (i + 1)
            pygame.draw.circle(glow_surface, (*glow_color, glow_alpha_layer), 
                             (glow_radius, glow_radius), glow_radius)
            ball_surface.blit(glow_surface, 
                            (surf_center_x - glow_radius, surf_center_y - glow_radius),
                            special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Draw main ball with transparency
        main_color = (*WHITE, decoy_ball.alpha)
        pygame.draw.circle(ball_surface, main_color, 
                         (surf_center_x, surf_center_y), decoy_ball.size)
        
        # Draw trail if it has one
        if decoy_ball.trail_positions:
            for i, (trail_x, trail_y) in enumerate(decoy_ball.trail_positions):
                trail_alpha = (i / len(decoy_ball.trail_positions)) * decoy_ball.alpha
                trail_size = max(1, int(decoy_ball.size * (i / len(decoy_ball.trail_positions))))
                trail_color = (*decoy_ball.trail_color, int(trail_alpha))
                
                # Draw trail point on ball surface (relative to ball position)
                rel_x = trail_x - decoy_ball.x + surf_center_x
                rel_y = trail_y - decoy_ball.y + surf_center_y
                
                if 0 <= rel_x < ball_surface.get_width() and 0 <= rel_y < ball_surface.get_height():
                    pygame.draw.circle(ball_surface, trail_color, (int(rel_x), int(rel_y)), trail_size)
        
        # Blit to main screen
        screen.blit(ball_surface, (decoy_ball.x - surf_center_x, decoy_ball.y - surf_center_y),
                   special_flags=pygame.BLEND_ALPHA_SDL2)
                   
    def render_wild_bounce_effect(self, particle_system, ball_x, ball_y):
        """Create particle effect when wild bounce occurs"""
        # Add chaotic particles in multiple directions
        for i in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            color = (255, 50, 0)  # Bright red-orange
            particle_system.add_particle(ball_x, ball_y, vx, vy, color, 20)

    def render_collection_effect(self, particle_system, x, y, powerup_type):
        """Create particle effect when power-up is collected"""
        # Choose color based on power-up type
        if powerup_type == POWERUP_PADDLE_SWAP:
            color = NEON_ORANGE
        elif powerup_type == POWERUP_GHOST_BALL:
            color = NEON_CYAN
        elif powerup_type == POWERUP_MAGNETIZE:
            color = NEON_YELLOW
        elif powerup_type == POWERUP_DECOY_BALL:
            color = (255, 100, 255)  # Bright magenta
        elif powerup_type == POWERUP_WILD_BOUNCE:
            color = (255, 50, 0)     # Bright red-orange
        elif powerup_type == POWERUP_CONTROL_SCRAMBLE:
            color = (100, 255, 100)  # Bright lime green
        else:
            color = NEON_PURPLE  # Classic power-ups
            
        # Add burst of particles
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            speed = 5
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle_system.add_particle(x, y, vx, vy, color, 30)