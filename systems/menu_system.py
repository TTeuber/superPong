from utils.constants import *

class MenuSystem:
    """Manages pause menu and other menu systems"""
    
    def __init__(self):
        # Pause menu state
        self.pause_menu_selected = PAUSE_MENU_RESUME  # Currently selected menu option
        self.menu_nav_pressed = False  # Track menu navigation input for single-press detection
        self.menu_confirm_pressed = False  # Track confirmation input for single-press detection
        self.menu_cancel_pressed = False  # Track cancel input for single-press detection
        
        # Callback functions for menu actions
        self.on_resume = None
        self.on_restart = None
        self.on_main_menu = None
        self.on_quit = None
        
    def set_callbacks(self, on_resume=None, on_restart=None, on_main_menu=None, on_quit=None):
        """Set callback functions for menu actions"""
        self.on_resume = on_resume
        self.on_restart = on_restart
        self.on_main_menu = on_main_menu
        self.on_quit = on_quit
        
    def get_selected_option(self):
        """Get the currently selected menu option"""
        return self.pause_menu_selected
        
    def handle_pause_menu_input(self, input_handler):
        """Handle input for pause menu navigation"""
        # Mouse support - check hover and clicks
        mouse_pos = input_handler.get_mouse_pos()
        
        # Define button positions (centered)
        button_y_start = SCREEN_HEIGHT // 2 - 60
        button_height = 40
        button_width = 200
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Check mouse hover and clicks
        for i, option in enumerate(PAUSE_MENU_OPTIONS):
            button_y = button_y_start + i * 60
            button_rect = (button_x, button_y, button_width, button_height)
            
            if input_handler.is_point_in_rect(mouse_pos, button_rect):
                self.pause_menu_selected = i
                
                # Check for click
                if input_handler.is_mouse_clicked():
                    self.execute_menu_action(i)
                    return
        
        # Original keyboard/controller navigation
        nav_direction = input_handler.get_menu_navigation()
        if nav_direction != 0:
            if not self.menu_nav_pressed:  # Only trigger on initial press
                self.pause_menu_selected = (self.pause_menu_selected + nav_direction) % len(PAUSE_MENU_OPTIONS)
                self.menu_nav_pressed = True
        else:
            self.menu_nav_pressed = False
            
        # Check for confirmation input
        if input_handler.is_menu_confirm_pressed():
            if not self.menu_confirm_pressed:  # Only trigger on initial press
                self.execute_menu_action(self.pause_menu_selected)
                self.menu_confirm_pressed = True
        else:
            self.menu_confirm_pressed = False
            
        # Check for cancel input (B button or ESC)
        if input_handler.is_menu_cancel_pressed():
            if not self.menu_cancel_pressed:  # Only trigger on initial press
                # B button or ESC cancels pause menu (same as Resume)
                self.execute_menu_action(PAUSE_MENU_RESUME)
                self.menu_cancel_pressed = True
        else:
            self.menu_cancel_pressed = False
            
    def execute_menu_action(self, action):
        """Execute the selected menu action"""
        if action == PAUSE_MENU_RESUME:
            if self.on_resume:
                self.on_resume()
        elif action == PAUSE_MENU_RESTART:
            if self.on_restart:
                self.on_restart()
        elif action == PAUSE_MENU_MAIN_MENU:
            if self.on_main_menu:
                self.on_main_menu()
        elif action == PAUSE_MENU_QUIT:
            if self.on_quit:
                self.on_quit()
                
    def reset_menu(self):
        """Reset menu to default state"""
        self.pause_menu_selected = PAUSE_MENU_RESUME  # Reset menu selection
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        self.menu_cancel_pressed = False