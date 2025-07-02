import pygame
import math
from utils.constants import *


class CoreGameRenderer:
    def __init__(self, ui_effects, effects_renderer):
        self.ui_effects = ui_effects
        self.effects_renderer = effects_renderer
        self.frame_count = 0

    def update_frame_count(self, frame_count):
        """Update frame count for animations"""
        self.frame_count = frame_count

    def draw_boundaries(self, screen):
        """Draw the game boundaries with pulsing glow"""
        # Calculate pulsing intensity for boundaries
        pulse = (math.sin(self.frame_count * 0.08) + 1) * 0.5  # Slower pulse than paddles
        glow_intensity = 0.8 + pulse * 0.2
        
        boundary_color = NEON_BLUE
        glow_alpha = int(80 * glow_intensity)
        
        boundaries = [
            (0, 0, SCREEN_WIDTH, BOUNDARY_THICKNESS),  # Top
            (0, SCREEN_HEIGHT - BOUNDARY_THICKNESS, SCREEN_WIDTH, BOUNDARY_THICKNESS),  # Bottom
            (0, 0, BOUNDARY_THICKNESS, SCREEN_HEIGHT),  # Left
            (SCREEN_WIDTH - BOUNDARY_THICKNESS, 0, BOUNDARY_THICKNESS, SCREEN_HEIGHT)  # Right
        ]
        
        for boundary in boundaries:
            x, y, w, h = boundary
            
            # Glow effect
            glow_surface = self.effects_renderer.create_glow_surface(w + 20, h + 20, boundary_color, glow_alpha)
            screen.blit(glow_surface, (x - 10, y - 10))
            
            # Main boundary
            pygame.draw.rect(screen, boundary_color, (x, y, w, h))

    def draw_paddle(self, screen, paddle, is_alive=True):
        """Draw a paddle with pulsing neon glow effect"""
        # Calculate pulsing intensity (dimmed for dead players)
        pulse = (math.sin(self.frame_count * 0.1) + 1) * 0.5  # 0 to 1
        base_intensity = 0.7 if is_alive else 0.2  # Much dimmer for dead players
        pulse_strength = 0.3 if is_alive else 0.1
        glow_intensity = base_intensity + pulse * pulse_strength
        
        # Dim colors for dead players
        paddle_color = paddle.color if is_alive else tuple(int(c * 0.3) for c in paddle.color)
        
        # Enhanced glow effect with multiple layers (reduced for dead players)
        glow_size = int(15 * glow_intensity)
        glow_alpha = int(120 * glow_intensity)
        
        paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
        
        if is_alive:  # Only show glow for alive players
            # Use effects renderer for multi-layer glow
            self.effects_renderer.draw_multi_layer_glow(screen, paddle_rect, paddle_color, glow_intensity)
        
        # Main paddle
        pygame.draw.rect(screen, paddle_color, paddle_rect)

        if is_alive:
            # Bright inner core with pulsing (only for alive players)
            core_brightness = int(50 * glow_intensity)
            inner_color = tuple(min(255, c + core_brightness) for c in paddle_color)
            inner_width = max(1, paddle.width - 4)
            inner_height = max(1, paddle.height - 4)
            pygame.draw.rect(screen, inner_color,
                             (paddle.x + 2, paddle.y + 2, inner_width, inner_height))

    def draw_ball(self, screen, ball):
        """Draw the ball with dynamic neon glow effect"""
        # Dynamic glow based on last paddle hit
        glow_radius = int((ball.size // 2 + 10) * ball.glow_intensity)
        glow_alpha = int(150 * ball.glow_intensity)
        
        # Use effects renderer for circular glow
        self.effects_renderer.draw_circular_glow(
            screen, 
            (int(ball.x), int(ball.y)), 
            ball.size // 2, 
            ball.last_hit_color, 
            ball.glow_intensity
        )
        
        # Main ball
        pygame.draw.circle(screen, WHITE, (int(ball.x), int(ball.y)), ball.size // 2)

        # Bright inner core with paddle color
        core_color = tuple(min(255, int(c * 0.7 + 255 * 0.3)) for c in ball.last_hit_color)
        pygame.draw.circle(screen, core_color, (int(ball.x), int(ball.y)), max(1, ball.size // 4))

    def draw_ball_trail(self, screen, ball):
        """Draw an enhanced trail behind the ball"""
        self.effects_renderer.draw_enhanced_trail(
            screen, 
            ball.trail_positions, 
            ball.size, 
            ball.last_hit_color
        )

    def draw_lives(self, screen, lives, alive_players):
        """Draw player lives in corners"""
        lives_positions = [
            (50, 50),                                    # Player 1 (top-left)
            (SCREEN_WIDTH - 150, 50),                    # Player 2 (top-right)
            (SCREEN_WIDTH // 2 - 50, 30),               # Player 3 (top-center)
            (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 60) # Player 4 (bottom-center)
        ]

        for i in range(4):
            x, y = lives_positions[i]
            color = PLAYER_COLORS[i] if alive_players[i] else tuple(int(c * 0.3) for c in PLAYER_COLORS[i])
            
            if alive_players[i]:
                # Show lives for alive players
                lives_text = f"Lives: {lives[i]}"
                text = self.ui_effects.font_medium.render(lives_text, True, color)
                screen.blit(text, (x, y))
            else:
                # Show "ELIMINATED" for dead players
                elim_text = "ELIMINATED"
                text = self.ui_effects.font_medium.render(elim_text, True, (100, 100, 100))
                screen.blit(text, (x, y))
                
                # Draw X over eliminated text
                pygame.draw.line(screen, (200, 0, 0), (x, y), (x + 120, y + 30), 3)
                pygame.draw.line(screen, (200, 0, 0), (x + 120, y), (x, y + 30), 3)

    def draw_aiming_system(self, screen, ball, aiming_player, aiming_angle, aiming_timer=0):
        """Draw aiming arrow and indicators"""
        # Draw aiming arrow
        arrow_length = 80
        arrow_start_x = ball.x
        arrow_start_y = ball.y
        
        # Calculate arrow end position
        angle_rad = math.radians(aiming_angle)
        arrow_end_x = arrow_start_x + math.cos(angle_rad) * arrow_length
        arrow_end_y = arrow_start_y + math.sin(angle_rad) * arrow_length
        
        # Draw arrow shaft
        arrow_color = PLAYER_COLORS[aiming_player]
        pygame.draw.line(screen, arrow_color, 
                        (arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y), 4)
        
        # Draw arrow head
        head_size = 15
        head_angle1 = aiming_angle + 150
        head_angle2 = aiming_angle - 150
        
        head1_x = arrow_end_x + math.cos(math.radians(head_angle1)) * head_size
        head1_y = arrow_end_y + math.sin(math.radians(head_angle1)) * head_size
        head2_x = arrow_end_x + math.cos(math.radians(head_angle2)) * head_size
        head2_y = arrow_end_y + math.sin(math.radians(head_angle2)) * head_size
        
        pygame.draw.line(screen, arrow_color, (arrow_end_x, arrow_end_y), (head1_x, head1_y), 3)
        pygame.draw.line(screen, arrow_color, (arrow_end_x, arrow_end_y), (head2_x, head2_y), 3)
        
        # Draw aiming circle around ball
        pygame.draw.circle(screen, arrow_color, (int(ball.x), int(ball.y)), 25, 2)
        
        # Draw "AIMING" text with angle information
        aiming_text = self.ui_effects.font_medium.render(f"Player {aiming_player + 1} AIMING ({aiming_angle:.1f}°)", True, arrow_color)
        text_x = SCREEN_WIDTH // 2 - aiming_text.get_width() // 2
        text_y = 100
        screen.blit(aiming_text, (text_x, text_y))
        
        # Draw aiming instructions
        if aiming_player == 0:  # Human player
            instruction = "Use W/S keys to aim the ball direction"
        else:  # AI player
            instruction = f"AI Player {aiming_player + 1} is aiming..."
        
        instr_text = self.ui_effects.font_small.render(instruction, True, (200, 200, 200))
        instr_x = SCREEN_WIDTH // 2 - instr_text.get_width() // 2
        instr_y = 130
        screen.blit(instr_text, (instr_x, instr_y))
        
        # Show countdown timer (calculate remaining time)
        remaining_time = max(0, int(aiming_timer / 60) + 1)
        timer_text = self.ui_effects.font_small.render(f"Auto-launch in: {remaining_time}s", True, (255, 255, 100))
        timer_x = SCREEN_WIDTH // 2 - timer_text.get_width() // 2
        timer_y = 155
        screen.blit(timer_text, (timer_x, timer_y))

    def draw_controls_info(self, screen, alive_players):
        """Draw control information (only for alive players)"""
        controls = [
            "P1: W/S", "P2: up/down", "P3: J/L", "P4: NUM4/6"
        ]

        y_offset = SCREEN_HEIGHT - 120
        x_offset = 0
        for i, control in enumerate(controls):
            if alive_players[i]:  # Only show controls for alive players
                color = PLAYER_COLORS[i]
                text = self.ui_effects.font_small.render(control, True, color)
                x_pos = 20 + x_offset * 150
                screen.blit(text, (x_pos, y_offset))
                x_offset += 1

    def render_game_elements(self, screen, paddles, ball, lives, alive_players, particle_system=None, 
                           game_state="playing", aiming_player=-1, aiming_angle=0, aiming_timer=0):
        """Render all core game elements"""
        # Clear screen with black background
        screen.fill(BLACK)

        # Draw background grid (delegate to ui_effects)
        self.ui_effects.draw_background_grid(screen, self.frame_count)

        # Draw boundaries
        self.draw_boundaries(screen)

        # Draw ball trail
        self.draw_ball_trail(screen, ball)

        # Draw ball
        self.draw_ball(screen, ball)

        # Draw paddles (only alive players, or dimmed for dead players)
        for i, paddle in enumerate(paddles):
            self.draw_paddle(screen, paddle, alive_players[i])

        # Draw particle effects
        if particle_system:
            particle_system.render(screen)

        # Draw lives
        self.draw_lives(screen, lives, alive_players)

        # Draw aiming system if in aiming mode
        if game_state == GAME_STATE_AIMING and aiming_player >= 0:
            self.draw_aiming_system(screen, ball, aiming_player, aiming_angle, aiming_timer)
        
        # Draw controls info (uncomment if needed)
        # self.draw_controls_info(screen, alive_players)