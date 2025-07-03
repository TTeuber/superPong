import pygame
import math
from utils.constants import *


class MenuRenderer:
    def __init__(self, ui_effects):
        self.ui_effects = ui_effects
        self.frame_count = 0

    def update_frame_count(self, frame_count):
        """Update frame count for animations"""
        self.frame_count = frame_count

    def draw_pause_overlay(self, screen, selected_option=0):
        """Draw navigable pause menu overlay with selection highlighting"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Calculate pulsing effect for selected option
        pulse = (math.sin(self.frame_count * 0.2) + 1) * 0.5  # 0 to 1
        selected_glow_intensity = 0.8 + pulse * 0.2
        
        # Main PAUSED text
        pause_text = "PAUSED"
        text_surface = self.ui_effects.font_large.render(pause_text, True, NEON_YELLOW)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        
        # Glow effect for pause text
        glow_size = 15
        glow_alpha = 80
        for i in range(3):
            glow_surface = pygame.Surface((text_rect.width + glow_size * 2, text_rect.height + glow_size * 2), pygame.SRCALPHA)
            glow_color = (*NEON_YELLOW, glow_alpha // (i + 1))
            glow_text = self.ui_effects.font_large.render(pause_text, True, glow_color)
            glow_text_rect = glow_text.get_rect(center=(glow_surface.get_width() // 2, glow_surface.get_height() // 2))
            glow_surface.blit(glow_text, glow_text_rect)
            screen.blit(glow_surface, (text_rect.x - glow_size, text_rect.y - glow_size))
        
        # Main pause text on top
        screen.blit(text_surface, text_rect)
        
        # Draw menu options
        menu_start_y = SCREEN_HEIGHT // 2 - 20
        option_spacing = 50
        
        for i, option_text in enumerate(PAUSE_MENU_OPTIONS):
            y_pos = menu_start_y + i * option_spacing
            
            # Determine colors based on selection
            if i == selected_option:
                # Selected option - bright with pulsing glow
                text_color = NEON_GREEN
                glow_color = NEON_GREEN
                glow_intensity = selected_glow_intensity
                font_to_use = self.ui_effects.font_large
                
                # Draw selection arrow
                arrow_text = "►"
                arrow_surface = self.ui_effects.font_large.render(arrow_text, True, NEON_GREEN)
                arrow_rect = arrow_surface.get_rect(center=(SCREEN_WIDTH // 2 - 120, y_pos))
                screen.blit(arrow_surface, arrow_rect)
                
            else:
                # Unselected option - dimmed
                text_color = NEON_BLUE
                glow_color = NEON_BLUE
                glow_intensity = 0.3
                font_to_use = self.ui_effects.font_medium
            
            # Create text surface
            text_surface = font_to_use.render(option_text, True, text_color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            
            # Draw glow effect for selected option
            if i == selected_option:
                glow_size = int(20 * glow_intensity)
                glow_alpha = int(120 * glow_intensity)
                for j in range(3):
                    glow_surface = pygame.Surface((text_rect.width + glow_size * 2, text_rect.height + glow_size * 2), pygame.SRCALPHA)
                    current_glow_color = (*glow_color, glow_alpha // (j + 1))
                    glow_text = font_to_use.render(option_text, True, current_glow_color)
                    glow_text_rect = glow_text.get_rect(center=(glow_surface.get_width() // 2, glow_surface.get_height() // 2))
                    glow_surface.blit(glow_text, glow_text_rect)
                    screen.blit(glow_surface, (text_rect.x - glow_size, text_rect.y - glow_size))
            
            # Draw main text
            screen.blit(text_surface, text_rect)
        
        # Instructions at bottom
        instruction_y = SCREEN_HEIGHT // 2 + 130
        instructions = [
            "Use ↑/↓ or Analog Stick to navigate",
            "Press A or ENTER to confirm",
            "Press B or ESC to cancel • START/P to quick resume"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.ui_effects.font_small.render(instruction, True, (150, 150, 150))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, instruction_y + i * 20))
            screen.blit(text_surface, text_rect)

    def render_start_screen(self, screen, start_screen_system):
        """Render the start screen with title, demo game, and menu"""
        # Clear screen with black background
        screen.fill(BLACK)
        
        # Draw subtle background grid - delegate to ui_effects
        self.ui_effects.draw_background_grid(screen, self.frame_count)
        
        # Get demo game state
        demo_state = start_screen_system.get_demo_game_state()
        
        # Draw split title "SUPER" and "PONG"
        title_words = ["SUPER", "PONG"]
        title_positions = [120, 280]  # Y positions for each word
        
        # Pulsing animation calculations
        pulse_time = self.frame_count * 0.05  # Slower pulse
        pulse_intensity = abs(math.sin(pulse_time)) * 0.6 + 0.4  # Range from 0.4 to 1.0
        color_cycle = self.frame_count * 0.02  # Color cycling
        
        # Create animated glow colors with rainbow effect
        base_colors = [NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_YELLOW, NEON_PURPLE]
        
        # Main title with color cycling
        title_color_index = int(color_cycle) % len(base_colors)
        next_color_index = (title_color_index + 1) % len(base_colors)
        color_blend = color_cycle - int(color_cycle)
        
        # Blend between two colors
        current_color = base_colors[title_color_index]
        next_color = base_colors[next_color_index]
        title_color = (
            int(current_color[0] * (1 - color_blend) + next_color[0] * color_blend),
            int(current_color[1] * (1 - color_blend) + next_color[1] * color_blend),
            int(current_color[2] * (1 - color_blend) + next_color[2] * color_blend)
        )
        
        # Draw each word of the title
        for word_idx, (word, y_pos) in enumerate(zip(title_words, title_positions)):
            # Create pulsing glow layers for this word
            glow_colors = []
            for i, base_color in enumerate(base_colors):
                # Create pulsing glow with varying intensities
                glow_alpha = int((pulse_intensity * 0.3 + 0.1) * 255)  # 10% to 40% opacity
                glow_color = (base_color[0] // 4, base_color[1] // 4, base_color[2] // 4, glow_alpha)
                glow_colors.append(glow_color)
            
            # Draw multiple animated glow layers for this word
            for i, glow_color in enumerate(glow_colors):
                glow_offset = math.sin(pulse_time + i * 0.5 + word_idx * 0.3) * 2  # Slight offset variation
                glow_surface = pygame.Surface((SCREEN_WIDTH, 150), pygame.SRCALPHA)
                glow_text = self.ui_effects.font_retro_massive.render(word, True, glow_color[:3])
                glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2 + glow_offset, 75))
                glow_surface.blit(glow_text, glow_rect)
                screen.blit(glow_surface, (0, y_pos - 75))
            
            # Draw main word with pulsing size
            scale_factor = 0.9 + pulse_intensity * 0.1  # Slight size pulsing
            word_surface = self.ui_effects.font_retro_massive.render(word, True, title_color)
            if scale_factor != 1.0:
                # Scale the word surface
                scaled_size = (int(word_surface.get_width() * scale_factor), 
                              int(word_surface.get_height() * scale_factor))
                word_surface = pygame.transform.scale(word_surface, scaled_size)
            
            word_rect = word_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(word_surface, word_rect)
        
        # Draw AI demo game at full screen scale (behind title and menu)
        
        # Draw demo paddles at actual game size
        for paddle in demo_state['paddles']:
            paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
            
            # Draw paddle glow
            glow_surface = pygame.Surface((paddle_rect.width + 20, paddle_rect.height + 20), pygame.SRCALPHA)
            glow_color = (*paddle.color, 60)
            pygame.draw.rect(glow_surface, glow_color, 
                           (10, 10, paddle_rect.width, paddle_rect.height))
            screen.blit(glow_surface, (paddle_rect.x - 10, paddle_rect.y - 10))
            
            # Draw main paddle
            pygame.draw.rect(screen, paddle.color, paddle_rect)
        
        # Draw demo ball at actual game size
        ball = demo_state['ball']
        
        # Draw ball glow
        glow_radius = int(ball.size * 2)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*WHITE, 40), (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surface, (ball.x - glow_radius, ball.y - glow_radius))
        
        # Draw main ball
        pygame.draw.circle(screen, WHITE, (int(ball.x), int(ball.y)), int(ball.size))
        
        # Draw menu options at bottom
        menu_y = 580  # Moved down more for larger menu text
        selected_option = start_screen_system.get_selected_option()
        
        for i, option in enumerate(START_MENU_OPTIONS):
            is_selected = (i == selected_option)
            
            # Create text surface
            if is_selected:
                text_surface = self.ui_effects.font_retro_large_menu.render(option, True, NEON_YELLOW)
            else:
                text_surface = self.ui_effects.font_retro_large_menu.render(option, True, WHITE)
            
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, menu_y + i * 70))  # Increased spacing for larger text
            
            # Draw glow for selected option
            if is_selected:
                # Pulsing glow effect
                pulse = abs(math.sin(self.frame_count * 0.1)) * 0.5 + 0.5
                glow_alpha = int(80 + pulse * 40)
                
                glow_size = 25  # Larger glow for larger text
                glow_surface = pygame.Surface((text_rect.width + glow_size * 2, 
                                             text_rect.height + glow_size * 2), pygame.SRCALPHA)
                glow_color = (*NEON_YELLOW, glow_alpha)
                glow_text = self.ui_effects.font_retro_large_menu.render(option, True, glow_color)
                glow_text_rect = glow_text.get_rect(center=(glow_surface.get_width() // 2, 
                                                          glow_surface.get_height() // 2))
                glow_surface.blit(glow_text, glow_text_rect)
                screen.blit(glow_surface, (text_rect.x - glow_size, text_rect.y - glow_size))
            
            # Draw main text
            screen.blit(text_surface, text_rect)
        
        # Draw instructions at bottom
        instruction_y = 720
        instructions = [
            "Use Up/Down or Analog Stick to navigate",
            "Press A or ENTER to select"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.ui_effects.font_small.render(instruction, True, (150, 150, 150))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, instruction_y + i * 20))
            screen.blit(text_surface, text_rect)

    def render_game_over_screen(self, screen, game_over_system):
        """Render the game over screen with winner announcement and menu"""
        # Clear screen with black background
        screen.fill(BLACK)
        
        # Draw subtle background grid
        self.ui_effects.draw_background_grid(screen, self.frame_count)
        
        # Get winner information
        winner_info = game_over_system.get_winner_info()
        winner_id = winner_info['winner_id']
        winner_message = winner_info['winner_message']
        celebration_timer = winner_info['celebration_timer']
        max_celebration_time = winner_info['max_celebration_time']
        
        # Draw "GAME OVER" title
        game_over_y = 120
        game_over_text = "GAME OVER"
        
        # Create pulsing effect for title
        pulse = abs(math.sin(self.frame_count * 0.08)) * 0.3 + 0.7
        title_glow_alpha = int(60 * pulse)
        
        # Draw multiple glow layers for title
        glow_colors = [
            (NEON_PURPLE[0] // 4, NEON_PURPLE[1] // 4, NEON_PURPLE[2] // 4),
            (NEON_ORANGE[0] // 3, NEON_ORANGE[1] // 3, NEON_ORANGE[2] // 3),
        ]
        
        for i, glow_color in enumerate(glow_colors):
            glow_size = 8 + i * 4
            glow_surface = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
            glow_text = self.ui_effects.font_retro_large.render(game_over_text, True, (*glow_color, title_glow_alpha))
            glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
            glow_surface.blit(glow_text, glow_rect)
            screen.blit(glow_surface, (0, game_over_y - 40))
        
        # Draw main title text
        title_surface = self.ui_effects.font_retro_large.render(game_over_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, game_over_y))
        screen.blit(title_surface, title_rect)
        
        # Draw winner announcement
        winner_y = 240
        if winner_id >= 0:
            # Get winner color
            winner_color = PLAYER_COLORS[winner_id]
            
            # Winner text with player color
            winner_text = f"PLAYER {winner_id + 1} WINS!"
            
            # Celebration effect - more intense early on
            celebration_intensity = celebration_timer / max_celebration_time
            celebration_glow_alpha = int(100 + celebration_intensity * 100)
            
            # Draw winner glow
            glow_size = 15
            glow_surface = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
            glow_text = self.ui_effects.font_retro_medium.render(winner_text, True, (*winner_color, celebration_glow_alpha))
            glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            glow_surface.blit(glow_text, glow_rect)
            screen.blit(glow_surface, (0, winner_y - 50))
            
            # Draw main winner text
            winner_surface = self.ui_effects.font_retro_medium.render(winner_text, True, winner_color)
            winner_rect = winner_surface.get_rect(center=(SCREEN_WIDTH // 2, winner_y))
            screen.blit(winner_surface, winner_rect)
            
            # Draw lives remaining info
            lives_y = winner_y + 60
            lives_text = f"Lives Remaining: {winner_info['winner_lives']}"
            lives_surface = self.ui_effects.font_small.render(lives_text, True, (200, 200, 200))
            lives_rect = lives_surface.get_rect(center=(SCREEN_WIDTH // 2, lives_y))
            screen.blit(lives_surface, lives_rect)
        else:
            # Draw tie/no winner message
            no_winner_text = "ALL PLAYERS ELIMINATED!"
            no_winner_surface = self.ui_effects.font_retro_medium.render(no_winner_text, True, NEON_PURPLE)
            no_winner_rect = no_winner_surface.get_rect(center=(SCREEN_WIDTH // 2, winner_y))
            screen.blit(no_winner_surface, no_winner_rect)
        
        # Draw celebration particles area (visual placeholder)
        if celebration_timer > 0:
            particle_area = pygame.Rect(200, 320, SCREEN_WIDTH - 400, 150)
            particle_alpha = int(celebration_intensity * 30)
            particle_surface = pygame.Surface((particle_area.width, particle_area.height), pygame.SRCALPHA)
            
            # Draw some simple celebration "sparks"
            import random
            for _ in range(int(20 * celebration_intensity)):
                x = random.randint(0, particle_area.width)
                y = random.randint(0, particle_area.height)
                color = random.choice(PLAYER_COLORS)
                size = random.randint(2, 5)
                pygame.draw.circle(particle_surface, (*color, particle_alpha), (x, y), size)
            
            screen.blit(particle_surface, particle_area.topleft)
        
        # Draw menu options at bottom
        menu_y = 550
        selected_option = game_over_system.get_selected_option()
        
        for i, option in enumerate(GAME_OVER_MENU_OPTIONS):
            is_selected = (i == selected_option)
            
            # Create text surface
            if is_selected:
                text_surface = self.ui_effects.font_retro_medium.render(option, True, NEON_YELLOW)
            else:
                text_surface = self.ui_effects.font_retro_medium.render(option, True, WHITE)
            
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, menu_y + i * 60))
            
            # Draw glow for selected option
            if is_selected:
                # Pulsing glow effect
                pulse = abs(math.sin(self.frame_count * 0.1)) * 0.5 + 0.5
                glow_alpha = int(80 + pulse * 40)
                
                glow_size = 20
                glow_surface = pygame.Surface((text_rect.width + glow_size * 2, 
                                             text_rect.height + glow_size * 2), pygame.SRCALPHA)
                glow_color = (*NEON_YELLOW, glow_alpha)
                glow_text = self.ui_effects.font_retro_medium.render(option, True, glow_color)
                glow_text_rect = glow_text.get_rect(center=(glow_surface.get_width() // 2, 
                                                          glow_surface.get_height() // 2))
                glow_surface.blit(glow_text, glow_text_rect)
                screen.blit(glow_surface, (text_rect.x - glow_size, text_rect.y - glow_size))
            
            # Draw main text
            screen.blit(text_surface, text_rect)
        
        # Draw instructions at bottom
        instruction_y = 760
        instructions = [
            "Use ↑/↓ or Analog Stick to navigate",
            "Press A or ENTER to select"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.ui_effects.font_small.render(instruction, True, (150, 150, 150))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, instruction_y + i * 20))
            screen.blit(text_surface, text_rect)

    def render_settings_screen(self, screen, settings_screen_system):
        """Render the settings screen with options and current values"""
        # Clear screen with black background
        screen.fill(BLACK)
        
        # Draw subtle background grid
        self.ui_effects.draw_background_grid(screen, self.frame_count)
        
        # Check if we're in power-up selection mode
        powerup_state = settings_screen_system.get_powerup_selection_state()
        
        if powerup_state['in_selection']:
            self.render_powerup_selection_screen(screen, powerup_state)
        else:
            self.render_main_settings_screen(screen, settings_screen_system)
    
    def render_main_settings_screen(self, screen, settings_screen_system):
        """Render the main settings screen with options and current values"""
        # Draw "SETTINGS" title at top
        title_y = 120
        title_text = "SETTINGS"
        
        # Create multiple glow layers for title
        glow_colors = [
            (NEON_GREEN[0] // 4, NEON_GREEN[1] // 4, NEON_GREEN[2] // 4),  # Dim green glow
            (NEON_PURPLE[0] // 3, NEON_PURPLE[1] // 3, NEON_PURPLE[2] // 3),  # Dim purple glow
        ]
        
        # Draw multiple glow layers for title
        for i, glow_color in enumerate(glow_colors):
            glow_size = 8 + i * 4
            glow_surface = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
            glow_text = self.ui_effects.font_retro_large.render(title_text, True, glow_color)
            glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
            glow_surface.blit(glow_text, glow_rect)
            screen.blit(glow_surface, (0, title_y - 40))
        
        # Draw main title text
        title_surface = self.ui_effects.font_retro_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, title_y))
        screen.blit(title_surface, title_rect)
        
        # Draw settings options
        menu_start_y = 280
        menu_spacing = 80
        selected_option = settings_screen_system.get_selected_option()
        
        for i, option in enumerate(SETTINGS_MENU_OPTIONS):
            is_selected = (i == selected_option)
            current_y = menu_start_y + i * menu_spacing
            
            # Get current value for this setting
            current_value = settings_screen_system.get_current_value(i)
            
            # Create option text
            option_text = option
            if is_selected:
                option_surface = self.ui_effects.font_retro_medium.render(option_text, True, NEON_YELLOW)
            else:
                option_surface = self.ui_effects.font_retro_medium.render(option_text, True, WHITE)
            
            # Position option text on the left
            option_rect = option_surface.get_rect()
            option_rect.right = SCREEN_WIDTH // 2 - 50
            option_rect.centery = current_y
            
            # Create value text (except for Back option)
            if i != SETTINGS_MENU_BACK:
                if is_selected:
                    value_surface = self.ui_effects.font_retro_medium.render(current_value, True, NEON_CYAN)
                else:
                    value_surface = self.ui_effects.font_retro_medium.render(current_value, True, (200, 200, 200))
                
                # Position value text on the right
                value_rect = value_surface.get_rect()
                value_rect.left = SCREEN_WIDTH // 2 + 50
                value_rect.centery = current_y
            
            # Draw glow for selected option
            if is_selected:
                # Pulsing glow effect
                pulse = abs(math.sin(self.frame_count * 0.1)) * 0.5 + 0.5
                glow_alpha = int(80 + pulse * 40)
                
                # Create glow for the entire row
                row_width = SCREEN_WIDTH - 200
                row_height = 50
                glow_surface = pygame.Surface((row_width, row_height), pygame.SRCALPHA)
                
                # Draw background glow
                glow_color = (*NEON_YELLOW, int(glow_alpha * 0.3))
                pygame.draw.rect(glow_surface, glow_color, 
                               (0, 0, row_width, row_height), border_radius=10)
                
                glow_rect = glow_surface.get_rect(center=(SCREEN_WIDTH // 2, current_y))
                screen.blit(glow_surface, glow_rect)
                
                # Draw arrows for changeable values (not for Back option)
                if i != SETTINGS_MENU_BACK:
                    # Left arrow
                    left_arrow_x = SCREEN_WIDTH // 2 + 20
                    arrow_y = current_y
                    arrow_color = NEON_YELLOW if is_selected else (100, 100, 100)
                    
                    # Draw left arrow
                    arrow_points = [
                        (left_arrow_x - 10, arrow_y),
                        (left_arrow_x, arrow_y - 8),
                        (left_arrow_x, arrow_y + 8)
                    ]
                    pygame.draw.polygon(screen, arrow_color, arrow_points)
                    
                    # Right arrow  
                    right_arrow_x = value_rect.right + 30
                    arrow_points = [
                        (right_arrow_x + 10, arrow_y),
                        (right_arrow_x, arrow_y - 8),
                        (right_arrow_x, arrow_y + 8)
                    ]
                    pygame.draw.polygon(screen, arrow_color, arrow_points)
            
            # Draw main option text
            screen.blit(option_surface, option_rect)
            
            # Draw value text (except for Back option)
            if i != SETTINGS_MENU_BACK:
                screen.blit(value_surface, value_rect)
        
        # Draw instructions at bottom
        instruction_y = 720
        instructions = [
            "Use ↑/↓ to navigate • Use ←/→ to change values",
            "Press ENTER to select • Press ESC to go back"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.ui_effects.font_small.render(instruction, True, (150, 150, 150))
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, instruction_y + i * 25))
            screen.blit(text_surface, text_rect)
    
    def render_powerup_selection_screen(self, screen, powerup_state):
        """Render the power-up selection screen with categories and toggles"""
        # Draw "POWER-UP SELECTION" title at top
        title_y = 120
        title_text = "POWER-UP SELECTION"
        
        # Create multiple glow layers for title
        glow_colors = [
            (NEON_PURPLE[0] // 4, NEON_PURPLE[1] // 4, NEON_PURPLE[2] // 4),  # Dim purple glow
            (NEON_ORANGE[0] // 3, NEON_ORANGE[1] // 3, NEON_ORANGE[2] // 3),  # Dim orange glow
        ]
        
        # Draw multiple glow layers for title
        for i, glow_color in enumerate(glow_colors):
            glow_size = 8 + i * 4
            glow_surface = pygame.Surface((SCREEN_WIDTH, 80), pygame.SRCALPHA)
            glow_text = self.ui_effects.font_retro_large.render(title_text, True, glow_color)
            glow_rect = glow_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
            glow_surface.blit(glow_text, glow_rect)
            screen.blit(glow_surface, (0, title_y - 40))
        
        # Draw main title text
        title_surface = self.ui_effects.font_retro_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, title_y))
        screen.blit(title_surface, title_rect)
        
        # Draw category selection at top
        category_y = 220
        category_names = list(POWERUP_CATEGORIES.keys())
        selected_category = powerup_state['category_selected']
        
        # Draw category selection with arrows
        category_text = f"◄ {category_names[selected_category]} ►"
        category_surface = self.ui_effects.font_retro_medium.render(category_text, True, NEON_CYAN)
        category_rect = category_surface.get_rect(center=(SCREEN_WIDTH // 2, category_y))
        
        # Draw glow for category
        pulse = abs(math.sin(self.frame_count * 0.1)) * 0.5 + 0.5
        glow_alpha = int(60 + pulse * 30)
        glow_surface = pygame.Surface((category_rect.width + 40, category_rect.height + 20), pygame.SRCALPHA)
        glow_color = (*NEON_CYAN, glow_alpha)
        glow_text = self.ui_effects.font_retro_medium.render(category_text, True, glow_color)
        glow_text_rect = glow_text.get_rect(center=(glow_surface.get_width() // 2, glow_surface.get_height() // 2))
        glow_surface.blit(glow_text, glow_text_rect)
        screen.blit(glow_surface, (category_rect.x - 20, category_rect.y - 10))
        
        screen.blit(category_surface, category_rect)
        
        # Get current category power-ups
        current_category_name = category_names[selected_category]
        current_powerups = POWERUP_CATEGORIES[current_category_name]
        selected_item = powerup_state['item_selected']
        enabled_powerups = powerup_state['enabled_powerups']
        
        # Draw power-up list
        powerup_start_y = 300
        powerup_spacing = 70
        
        for i, powerup_type in enumerate(current_powerups):
            is_selected = (i == selected_item)
            is_enabled = powerup_type in enabled_powerups
            current_y = powerup_start_y + i * powerup_spacing
            
            # Get power-up display name (remove prefix for cleaner display)
            display_name = powerup_type.replace('_', ' ').title()
            
            # Create status indicator
            status_text = "✓ ON" if is_enabled else "✗ OFF"
            status_color = NEON_GREEN if is_enabled else NEON_PINK
            
            # Create main text color based on selection and status
            if is_selected:
                name_color = NEON_YELLOW
                description_color = NEON_CYAN
            else:
                name_color = WHITE if is_enabled else (150, 150, 150)
                description_color = (200, 200, 200) if is_enabled else (120, 120, 120)
            
            # Draw power-up name
            name_surface = self.ui_effects.font_retro_medium.render(display_name, True, name_color)
            name_rect = name_surface.get_rect()
            name_rect.left = 150
            name_rect.centery = current_y - 15
            
            # Draw status
            status_surface = self.ui_effects.font_medium.render(status_text, True, status_color)
            status_rect = status_surface.get_rect()
            status_rect.right = SCREEN_WIDTH - 150
            status_rect.centery = current_y - 15
            
            # Draw description
            description = POWERUP_DESCRIPTIONS.get(powerup_type, "No description available")
            description_surface = self.ui_effects.font_small.render(description, True, description_color)
            description_rect = description_surface.get_rect()
            description_rect.left = 150
            description_rect.centery = current_y + 15
            
            # Draw selection glow
            if is_selected:
                # Create glow for the entire power-up row
                row_width = SCREEN_WIDTH - 200
                row_height = 60
                glow_surface = pygame.Surface((row_width, row_height), pygame.SRCALPHA)
                
                # Draw background glow
                pulse_glow_alpha = int(40 + pulse * 30)
                glow_color = (*NEON_YELLOW, pulse_glow_alpha)
                pygame.draw.rect(glow_surface, glow_color, 
                               (0, 0, row_width, row_height), border_radius=10)
                
                glow_rect = glow_surface.get_rect(center=(SCREEN_WIDTH // 2, current_y))
                screen.blit(glow_surface, glow_rect)
                
                # Draw selection arrow
                arrow_text = "►"
                arrow_surface = self.ui_effects.font_retro_medium.render(arrow_text, True, NEON_YELLOW)
                arrow_rect = arrow_surface.get_rect()
                arrow_rect.right = 130
                arrow_rect.centery = current_y - 15
                screen.blit(arrow_surface, arrow_rect)
            
            # Draw main text elements
            screen.blit(name_surface, name_rect)
            screen.blit(status_surface, status_rect)
            screen.blit(description_surface, description_rect)
        
        # Draw instructions at bottom
        instruction_y = 680
        instructions = [
            "Use ↑/↓ to navigate power-ups • Use ←/→ to switch categories",
            "Press ENTER to toggle power-up • Press ESC to go back",
            f"Enabled: {len(enabled_powerups)}/{len(POWERUP_ALL_TYPES)} power-ups"
        ]
        
        for i, instruction in enumerate(instructions):
            color = (150, 150, 150) if i < 2 else NEON_GREEN
            text_surface = self.ui_effects.font_small.render(instruction, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, instruction_y + i * 25))
            screen.blit(text_surface, text_rect)