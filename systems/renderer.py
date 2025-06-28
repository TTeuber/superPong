import pygame
from utils.constants import *

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.frame_count = 0  # For animation timing
        
        # Screen shake effects
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

        # Initialize fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

    def render_frame(self, paddles, ball, lives, alive_players, particle_system=None, 
                   game_state="playing", aiming_player=-1, aiming_angle=0, aiming_timer=0):
        """Render a complete game frame with screen shake"""
        self.frame_count += 1
        
        # Update screen shake
        self.update_screen_shake()
        
        # Create a surface for the main game content
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        original_screen = self.screen
        self.screen = game_surface  # Temporarily redirect drawing to the game surface
        
        # Clear screen with black background
        self.screen.fill(BLACK)

        # Draw background grid
        self.draw_background_grid()

        # Draw boundaries
        self.draw_boundaries()

        # Draw ball trail
        self.draw_ball_trail(ball)

        # Draw ball
        self.draw_ball(ball)

        # Draw paddles (only alive players, or dimmed for dead players)
        for i, paddle in enumerate(paddles):
            self.draw_paddle(paddle, alive_players[i])

        # Draw particle effects
        if particle_system:
            particle_system.render(self.screen)

        # Draw lives
        self.draw_lives(lives, alive_players)

        # Draw aiming system if in aiming mode
        if game_state == GAME_STATE_AIMING and aiming_player >= 0:
            self.draw_aiming_system(ball, aiming_player, aiming_angle, aiming_timer)
        
        # Draw controls info
        self.draw_controls_info(alive_players)
        
        # Restore original screen and blit with shake offset
        self.screen = original_screen
        self.screen.fill(BLACK)  # Clear the main screen
        self.screen.blit(game_surface, (self.shake_offset_x, self.shake_offset_y))
    
    def add_screen_shake(self, intensity, duration):
        """Add screen shake effect"""
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_duration = max(self.shake_duration, duration)
    
    def update_screen_shake(self):
        """Update screen shake offset"""
        import random
        
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
    
    def draw_aiming_system(self, ball, aiming_player, aiming_angle, aiming_timer=0):
        """Draw aiming arrow and indicators"""
        import math
        
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
        pygame.draw.line(self.screen, arrow_color, 
                        (arrow_start_x, arrow_start_y), (arrow_end_x, arrow_end_y), 4)
        
        # Draw arrow head
        head_size = 15
        head_angle1 = aiming_angle + 150
        head_angle2 = aiming_angle - 150
        
        head1_x = arrow_end_x + math.cos(math.radians(head_angle1)) * head_size
        head1_y = arrow_end_y + math.sin(math.radians(head_angle1)) * head_size
        head2_x = arrow_end_x + math.cos(math.radians(head_angle2)) * head_size
        head2_y = arrow_end_y + math.sin(math.radians(head_angle2)) * head_size
        
        pygame.draw.line(self.screen, arrow_color, (arrow_end_x, arrow_end_y), (head1_x, head1_y), 3)
        pygame.draw.line(self.screen, arrow_color, (arrow_end_x, arrow_end_y), (head2_x, head2_y), 3)
        
        # Draw aiming circle around ball
        pygame.draw.circle(self.screen, arrow_color, (int(ball.x), int(ball.y)), 25, 2)
        
        # Draw "AIMING" text with angle information
        aiming_text = self.font_medium.render(f"Player {aiming_player + 1} AIMING ({aiming_angle:.1f}°)", True, arrow_color)
        text_x = SCREEN_WIDTH // 2 - aiming_text.get_width() // 2
        text_y = 100
        self.screen.blit(aiming_text, (text_x, text_y))
        
        # Draw aiming instructions
        if aiming_player == 0:  # Human player
            instruction = "Use W/S keys to aim the ball direction"
        else:  # AI player
            instruction = f"AI Player {aiming_player + 1} is aiming..."
        
        instr_text = self.font_small.render(instruction, True, (200, 200, 200))
        instr_x = SCREEN_WIDTH // 2 - instr_text.get_width() // 2
        instr_y = 130
        self.screen.blit(instr_text, (instr_x, instr_y))
        
        # Show countdown timer (calculate remaining time)
        remaining_time = max(0, int(aiming_timer / 60) + 1)
        timer_text = self.font_small.render(f"Auto-launch in: {remaining_time}s", True, (255, 255, 100))
        timer_x = SCREEN_WIDTH // 2 - timer_text.get_width() // 2
        timer_y = 155
        self.screen.blit(timer_text, (timer_x, timer_y))

    def draw_background_grid(self):
        """Draw an animated neon grid background"""
        import math
        
        # Pulsing grid intensity
        pulse = (math.sin(self.frame_count * 0.05) + 1) * 0.5
        base_intensity = 50
        grid_intensity = int(base_intensity + pulse * 20)
        
        grid_color = (0, grid_intensity, grid_intensity)
        grid_spacing = 50
        
        # Moving grid offset for subtle animation
        offset = int(self.frame_count * 0.2) % grid_spacing

        # Vertical lines with movement
        for x in range(-offset, SCREEN_WIDTH + grid_spacing, grid_spacing):
            if 0 <= x <= SCREEN_WIDTH:
                pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)

        # Horizontal lines with movement
        for y in range(-offset, SCREEN_HEIGHT + grid_spacing, grid_spacing):
            if 0 <= y <= SCREEN_HEIGHT:
                pygame.draw.line(self.screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)

        # Center lines with enhanced pulsing
        center_pulse = (math.sin(self.frame_count * 0.12) + 1) * 0.5
        center_intensity = int(100 + center_pulse * 50)
        center_color = (0, center_intensity, center_intensity)
        
        pygame.draw.line(self.screen, center_color,
                         (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.screen, center_color,
                         (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2), 2)
        
        # Grid intersection highlights
        for x in range(0, SCREEN_WIDTH, grid_spacing * 2):
            for y in range(0, SCREEN_HEIGHT, grid_spacing * 2):
                highlight_alpha = int(30 * pulse)
                if highlight_alpha > 0:
                    highlight_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                    highlight_color = (*NEON_BLUE, highlight_alpha)
                    pygame.draw.circle(highlight_surface, highlight_color, (3, 3), 3)
                    self.screen.blit(highlight_surface, (x - 3, y - 3))

    def draw_boundaries(self):
        """Draw the game boundaries with pulsing glow"""
        import math
        
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
            glow_surface = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
            glow_color = (*boundary_color, glow_alpha)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, w + 20, h + 20))
            self.screen.blit(glow_surface, (x - 10, y - 10))
            
            # Main boundary
            pygame.draw.rect(self.screen, boundary_color, (x, y, w, h))

    def draw_paddle(self, paddle, is_alive=True):
        """Draw a paddle with pulsing neon glow effect"""
        import math
        
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
        
        if is_alive:  # Only show glow for alive players
            # Outer glow
            outer_glow_surface = pygame.Surface((paddle.width + glow_size * 2, paddle.height + glow_size * 2), pygame.SRCALPHA)
            outer_glow_color = (*paddle_color, glow_alpha // 3)
            pygame.draw.rect(outer_glow_surface, outer_glow_color,
                            (0, 0, paddle.width + glow_size * 2, paddle.height + glow_size * 2))
            self.screen.blit(outer_glow_surface, (paddle.x - glow_size, paddle.y - glow_size))
            
            # Inner glow
            inner_glow_surface = pygame.Surface((paddle.width + 10, paddle.height + 10), pygame.SRCALPHA)
            inner_glow_color = (*paddle_color, glow_alpha)
            pygame.draw.rect(inner_glow_surface, inner_glow_color,
                            (0, 0, paddle.width + 10, paddle.height + 10))
            self.screen.blit(inner_glow_surface, (paddle.x - 5, paddle.y - 5))
        
        # Main paddle
        pygame.draw.rect(self.screen, paddle_color,
                         (paddle.x, paddle.y, paddle.width, paddle.height))

        if is_alive:
            # Bright inner core with pulsing (only for alive players)
            core_brightness = int(50 * glow_intensity)
            inner_color = tuple(min(255, c + core_brightness) for c in paddle_color)
            inner_width = max(1, paddle.width - 4)
            inner_height = max(1, paddle.height - 4)
            pygame.draw.rect(self.screen, inner_color,
                             (paddle.x + 2, paddle.y + 2, inner_width, inner_height))

    def draw_ball(self, ball):
        """Draw the ball with dynamic neon glow effect"""
        # Dynamic glow based on last paddle hit
        glow_radius = int((ball.size // 2 + 10) * ball.glow_intensity)
        glow_alpha = int(150 * ball.glow_intensity)
        
        # Multiple glow layers for more dramatic effect
        glow_surface = pygame.Surface((glow_radius * 2 + 10, glow_radius * 2 + 10), pygame.SRCALPHA)
        
        # Outer glow
        outer_glow_color = (*ball.last_hit_color, glow_alpha // 3)
        pygame.draw.circle(glow_surface, outer_glow_color,
                          (glow_radius + 5, glow_radius + 5), glow_radius)
        
        # Inner glow
        inner_glow_color = (*ball.last_hit_color, glow_alpha // 2)
        pygame.draw.circle(glow_surface, inner_glow_color,
                          (glow_radius + 5, glow_radius + 5), glow_radius // 2)
        
        self.screen.blit(glow_surface, (ball.x - glow_radius - 5, ball.y - glow_radius - 5))
        
        # Main ball
        pygame.draw.circle(self.screen, WHITE, (int(ball.x), int(ball.y)), ball.size // 2)

        # Bright inner core with paddle color
        core_color = tuple(min(255, int(c * 0.7 + 255 * 0.3)) for c in ball.last_hit_color)
        pygame.draw.circle(self.screen, core_color, (int(ball.x), int(ball.y)), max(1, ball.size // 4))

    def draw_ball_trail(self, ball):
        """Draw an enhanced trail behind the ball"""
        if len(ball.trail_positions) < 2:
            return

        for i, pos in enumerate(ball.trail_positions):
            progress = i / len(ball.trail_positions)
            alpha = int(255 * progress * 0.7)  # Increased trail visibility
            
            if alpha > 0:
                # Use the ball's current color for trail
                trail_color = (*ball.last_hit_color, alpha)
                trail_size = int(ball.size * (0.3 + progress * 0.7))  # Variable size trail
                
                trail_surface = pygame.Surface((trail_size * 2, trail_size * 2), pygame.SRCALPHA)
                
                # Add glow to trail segments
                glow_alpha = alpha // 3
                if glow_alpha > 0:
                    glow_color = (*ball.last_hit_color, glow_alpha)
                    pygame.draw.circle(trail_surface, glow_color,
                                     (trail_size, trail_size), trail_size)
                
                # Main trail segment
                pygame.draw.circle(trail_surface, trail_color,
                                 (trail_size, trail_size), trail_size // 2)
                
                self.screen.blit(trail_surface, (pos[0] - trail_size, pos[1] - trail_size))

    def draw_lives(self, lives, alive_players):
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
                text = self.font_medium.render(lives_text, True, color)
                self.screen.blit(text, (x, y))
            else:
                # Show "ELIMINATED" for dead players
                elim_text = "ELIMINATED"
                text = self.font_medium.render(elim_text, True, (100, 100, 100))
                self.screen.blit(text, (x, y))
                
                # Draw X over eliminated text
                pygame.draw.line(self.screen, (200, 0, 0), (x, y), (x + 120, y + 30), 3)
                pygame.draw.line(self.screen, (200, 0, 0), (x + 120, y), (x, y + 30), 3)

    def draw_controls_info(self, alive_players):
        """Draw control information (only for alive players)"""
        controls = [
            "P1: W/S", "P2: ↑/↓", "P3: J/L", "P4: NUM4/6"
        ]

        y_offset = SCREEN_HEIGHT - 120
        x_offset = 0
        for i, control in enumerate(controls):
            if alive_players[i]:  # Only show controls for alive players
                color = PLAYER_COLORS[i]
                text = self.font_small.render(control, True, color)
                x_pos = 20 + x_offset * 150
                self.screen.blit(text, (x_pos, y_offset))
                x_offset += 1