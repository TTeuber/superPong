from utils.constants import *

class GameOverSystem:
    """Manages the game over screen with winner display and menu navigation"""
    
    def __init__(self):
        # Menu state
        self.game_over_menu_selected = GAME_OVER_RESTART
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        
        # Winner information
        self.winner_id = -1
        self.winner_lives = 0
        self.winner_message = ""
        
        # Callback functions
        self.on_restart = None
        self.on_main_menu = None
        self.on_quit = None
        
        # Visual effects
        self.celebration_timer = 0
        self.max_celebration_time = 300  # 5 seconds at 60 FPS
        
    def set_callbacks(self, on_restart=None, on_main_menu=None, on_quit=None):
        """Set callback functions for menu actions"""
        self.on_restart = on_restart
        self.on_main_menu = on_main_menu
        self.on_quit = on_quit
        
    def set_winner_info(self, winner_id, winner_lives, winner_message):
        """Set the winner information for display"""
        self.winner_id = winner_id
        self.winner_lives = winner_lives
        self.winner_message = winner_message
        self.celebration_timer = self.max_celebration_time
        
    def get_selected_option(self):
        """Get the currently selected menu option"""
        return self.game_over_menu_selected
        
    def get_winner_info(self):
        """Get winner information for rendering"""
        return {
            'winner_id': self.winner_id,
            'winner_lives': self.winner_lives,
            'winner_message': self.winner_message,
            'celebration_timer': self.celebration_timer,
            'max_celebration_time': self.max_celebration_time
        }
        
    def handle_game_over_input(self, input_handler):
        """Handle input for game over menu navigation"""
        # Mouse support - check hover and clicks
        mouse_pos = input_handler.get_mouse_pos()
        
        # Define button positions (centered)
        button_y_start = SCREEN_HEIGHT // 2 + 100
        button_height = 40
        button_width = 250
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Check mouse hover and clicks
        for i, option in enumerate(GAME_OVER_MENU_OPTIONS):
            button_y = button_y_start + i * 60
            button_rect = (button_x, button_y, button_width, button_height)
            
            if input_handler.is_point_in_rect(mouse_pos, button_rect):
                self.game_over_menu_selected = i
                
                # Check for click
                if input_handler.is_mouse_clicked():
                    print(f"Game Over: Selected '{GAME_OVER_MENU_OPTIONS[i]}'")
                    self.execute_menu_action(i)
                    return
        
        # Original keyboard/controller navigation
        nav_direction = input_handler.get_menu_navigation()
        if nav_direction != 0:
            if not self.menu_nav_pressed:
                old_selection = self.game_over_menu_selected
                # Navigate menu
                self.game_over_menu_selected = (self.game_over_menu_selected + nav_direction) % len(GAME_OVER_MENU_OPTIONS)
                print(f"Game Over Menu: {GAME_OVER_MENU_OPTIONS[old_selection]} -> {GAME_OVER_MENU_OPTIONS[self.game_over_menu_selected]}")
                self.menu_nav_pressed = True
        else:
            self.menu_nav_pressed = False
            
        # Check for confirmation input
        if input_handler.is_menu_confirm_pressed():
            if not self.menu_confirm_pressed:
                print(f"Game Over: Selected '{GAME_OVER_MENU_OPTIONS[self.game_over_menu_selected]}'")
                self.execute_menu_action(self.game_over_menu_selected)
                self.menu_confirm_pressed = True
        else:
            self.menu_confirm_pressed = False
            
    def execute_menu_action(self, action):
        """Execute the selected menu action"""
        if action == GAME_OVER_RESTART:
            if self.on_restart:
                self.on_restart()
        elif action == GAME_OVER_MAIN_MENU:
            if self.on_main_menu:
                self.on_main_menu()
        elif action == GAME_OVER_QUIT:
            if self.on_quit:
                self.on_quit()
                
    def update(self):
        """Update game over screen effects"""
        if self.celebration_timer > 0:
            self.celebration_timer -= 1
            
    def reset(self):
        """Reset game over system"""
        self.game_over_menu_selected = GAME_OVER_RESTART
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        self.winner_id = -1
        self.winner_lives = 0
        self.winner_message = ""
        self.celebration_timer = 0