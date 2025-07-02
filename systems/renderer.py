import pygame
from utils.constants import *
from ui.ui_effects import UIEffects
from ui.menu_renderer import MenuRenderer
from systems.game_renderer import CoreGameRenderer
from systems.effects_renderer import EffectsRenderer

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.frame_count = 0  # For animation timing
        
        # Initialize specialized renderers
        self.ui_effects = UIEffects()
        self.effects_renderer = EffectsRenderer()
        self.game_renderer = CoreGameRenderer(self.ui_effects, self.effects_renderer)
        self.menu_renderer = MenuRenderer(self.ui_effects)

    def render_frame(self, paddles, ball, lives, alive_players, particle_system=None, 
                   game_state="playing", aiming_player=-1, aiming_angle=0, aiming_timer=0, pause_menu_selected=0):
        """Render a complete game frame with screen shake"""
        self.frame_count += 1
        
        # Update frame count in all renderers
        self.game_renderer.update_frame_count(self.frame_count)
        self.menu_renderer.update_frame_count(self.frame_count)
        
        # Update screen shake
        self.effects_renderer.update_screen_shake()
        
        # Create a surface for the main game content
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Render game elements to the game surface
        self.game_renderer.render_game_elements(
            game_surface, paddles, ball, lives, alive_players, particle_system,
            game_state, aiming_player, aiming_angle, aiming_timer
        )
        
        # Draw pause overlay if paused
        if game_state == GAME_STATE_PAUSED:
            self.menu_renderer.draw_pause_overlay(game_surface, pause_menu_selected)
        
        # Apply screen shake and blit to main screen
        self.effects_renderer.apply_shake_to_surface(self.screen, game_surface)
    
    def add_screen_shake(self, intensity, duration):
        """Add screen shake effect"""
        self.effects_renderer.add_screen_shake(intensity, duration)
    
            
    def render_start_screen(self, start_screen_system):
        """Render the start screen with title, demo game, and menu"""
        self.frame_count += 1
        self.menu_renderer.update_frame_count(self.frame_count)
        
        self.menu_renderer.render_start_screen(self.screen, start_screen_system)
            
    def render_game_over_screen(self, game_over_system):
        """Render the game over screen with winner announcement and menu"""
        self.frame_count += 1
        self.menu_renderer.update_frame_count(self.frame_count)
        
        self.menu_renderer.render_game_over_screen(self.screen, game_over_system)

    def render_settings_screen(self, settings_screen_system):
        """Render the settings screen with options and current values"""
        self.frame_count += 1
        self.menu_renderer.update_frame_count(self.frame_count)
        
        self.menu_renderer.render_settings_screen(self.screen, settings_screen_system)