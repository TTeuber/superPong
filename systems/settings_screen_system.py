from utils import constants

class SettingsScreenSystem:
    """Manages the settings screen with menu navigation and value changes"""
    
    def __init__(self):
        # Menu state
        self.settings_menu_selected = constants.SETTINGS_MENU_DIFFICULTY
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        self.value_change_pressed = False
        
        # Callback functions
        self.on_back = None
        self.on_setting_changed = None
        
        # Current settings values (will be loaded from settings system)
        self.current_difficulty = constants.DIFFICULTY_MEDIUM
        self.current_sound_enabled = True
        self.current_controller_sensitivity = 1.0
        self.current_powerups_enabled = True
        self.current_screen_scale = 1.0  # Will be properly loaded in load_current_settings
        
    def set_callbacks(self, on_back=None, on_setting_changed=None):
        """Set callback functions for menu actions"""
        self.on_back = on_back
        self.on_setting_changed = on_setting_changed
        
    def load_current_settings(self, settings_system):
        """Load current settings from the settings system"""
        if settings_system:
            difficulty_value = settings_system.get_setting('ai_difficulty')
            # Find difficulty name from value
            for name, value in constants.DIFFICULTY_VALUES.items():
                if abs(value - difficulty_value) < 0.01:  # Float comparison
                    self.current_difficulty = name
                    break
            
            self.current_sound_enabled = settings_system.get_setting('sound_enabled')
            self.current_controller_sensitivity = settings_system.get_setting('controller_sensitivity')
            self.current_powerups_enabled = settings_system.get_setting('powerups_enabled')
            self.current_screen_scale = settings_system.get_setting('screen_scale')
            
    def sync_screen_scale(self, settings_system):
        """Synchronize current screen scale with actual settings value"""
        if settings_system:
            actual_scale = settings_system.get_setting('screen_scale')
            if actual_scale != self.current_screen_scale:
                print(f"[DEBUG] Syncing screen scale: {self.current_screen_scale} -> {actual_scale}")
                self.current_screen_scale = actual_scale
        
    def get_selected_option(self):
        """Get the currently selected menu option"""
        return self.settings_menu_selected
        
    def get_current_value(self, option):
        """Get the current value for a settings option"""
        if option == constants.SETTINGS_MENU_DIFFICULTY:
            return self.current_difficulty
        elif option == constants.SETTINGS_MENU_SOUND:
            return "On" if self.current_sound_enabled else "Off"
        elif option == constants.SETTINGS_MENU_CONTROLLER:
            return f"{self.current_controller_sensitivity:.1f}"
        elif option == constants.SETTINGS_MENU_POWERUPS:
            return "On" if self.current_powerups_enabled else "Off"
        elif option == constants.SETTINGS_MENU_SCREEN_SIZE:
            # Show as percentage
            return f"{int(self.current_screen_scale * 100)}%"
        return ""
        
    def handle_settings_input(self, input_handler):
        """Handle input for settings menu navigation"""
        self.handle_main_settings_input(input_handler)
    
    def handle_main_settings_input(self, input_handler):
        """Handle input for main settings menu"""
        # Mouse support - check hover and clicks
        mouse_pos = input_handler.get_mouse_pos()
        
        # Define button positions (match rendering in menu_renderer.py)
        button_y_start = 280  # Matches menu_start_y in menu_renderer.py
        button_height = 40
        button_width = 500
        button_x = constants.SCREEN_WIDTH // 2 - button_width // 2
        arrow_width = 40
        
        # Check mouse hover and clicks on options
        for i, option in enumerate(constants.SETTINGS_MENU_OPTIONS):
            button_y = button_y_start + i * 80  # Matches menu_spacing in menu_renderer.py
            button_rect = (button_x, button_y, button_width, button_height)
            
            if input_handler.is_point_in_rect(mouse_pos, button_rect):
                self.settings_menu_selected = i
                
                # Check for click on option
                if input_handler.is_mouse_clicked():
                    if option == constants.SETTINGS_MENU_BACK:
                        self.execute_menu_action(option)
                        return
                    elif option == constants.SETTINGS_MENU_POWERUPS:
                        self.execute_menu_action(option)
                        return
                        
                # Check for clicks on left/right arrows for value changes
                left_arrow_rect = (button_x - arrow_width - 10, button_y, arrow_width, button_height)
                right_arrow_rect = (button_x + button_width + 10, button_y, arrow_width, button_height)
                
                if input_handler.is_mouse_clicked():
                    if input_handler.is_point_in_rect(mouse_pos, left_arrow_rect):
                        self.change_setting_value(option, -1)
                    elif input_handler.is_point_in_rect(mouse_pos, right_arrow_rect):
                        self.change_setting_value(option, 1)
        
        # Original keyboard/controller navigation
        nav_direction = input_handler.get_menu_navigation()
        if nav_direction != 0:
            if not self.menu_nav_pressed:
                # Navigate menu
                self.settings_menu_selected = (self.settings_menu_selected + nav_direction) % len(constants.SETTINGS_MENU_OPTIONS)
                self.menu_nav_pressed = True
        else:
            self.menu_nav_pressed = False
            
        # Check for value changes (left/right)
        value_direction = input_handler.get_horizontal_navigation()
        if value_direction != 0:
            if not self.value_change_pressed:
                self.change_setting_value(self.settings_menu_selected, value_direction)
                self.value_change_pressed = True
        else:
            self.value_change_pressed = False
            
        # Check for confirmation input
        if input_handler.is_menu_confirm_pressed():
            if not self.menu_confirm_pressed:
                self.execute_menu_action(self.settings_menu_selected)
                self.menu_confirm_pressed = True
        else:
            self.menu_confirm_pressed = False
            
        # Check for back/escape input
        if input_handler.is_menu_cancel_pressed():
            if self.on_back:
                self.on_back()
                
    def change_setting_value(self, setting_option, direction):
        """Change the value of a setting option"""
        if setting_option == constants.SETTINGS_MENU_DIFFICULTY:
            current_index = constants.DIFFICULTY_OPTIONS.index(self.current_difficulty)
            new_index = (current_index + direction) % len(constants.DIFFICULTY_OPTIONS)
            self.current_difficulty = constants.DIFFICULTY_OPTIONS[new_index]
            
            # Notify settings changed
            if self.on_setting_changed:
                self.on_setting_changed('ai_difficulty', constants.DIFFICULTY_VALUES[self.current_difficulty])
                
        elif setting_option == constants.SETTINGS_MENU_SOUND:
            self.current_sound_enabled = not self.current_sound_enabled
            
            # Notify settings changed
            if self.on_setting_changed:
                self.on_setting_changed('sound_enabled', self.current_sound_enabled)
                
        elif setting_option == constants.SETTINGS_MENU_CONTROLLER:
            # Change sensitivity in 0.1 increments between 0.5 and 2.0
            sensitivity_step = 0.1 * direction
            new_sensitivity = self.current_controller_sensitivity + sensitivity_step
            new_sensitivity = max(0.5, min(2.0, new_sensitivity))  # Clamp between 0.5 and 2.0
            self.current_controller_sensitivity = round(new_sensitivity, 1)
            
            # Notify settings changed
            if self.on_setting_changed:
                self.on_setting_changed('controller_sensitivity', self.current_controller_sensitivity)
                
        elif setting_option == constants.SETTINGS_MENU_POWERUPS:
            # Toggle powerups on/off
            self.current_powerups_enabled = not self.current_powerups_enabled
            
            # Notify settings changed
            if self.on_setting_changed:
                self.on_setting_changed('powerups_enabled', self.current_powerups_enabled)
                
        elif setting_option == constants.SETTINGS_MENU_SCREEN_SIZE:
            # Change screen scale in 5% increments between 50% and 150%
            increment = 0.05 * direction
            old_scale = self.current_screen_scale
            new_scale = self.current_screen_scale + increment
            new_scale = max(0.5, min(1.5, new_scale))  # Clamp between 0.5 and 1.5
            self.current_screen_scale = round(new_scale, 2)
            print(f"[DEBUG] Settings screen scale change: {old_scale} -> {self.current_screen_scale} (increment: {increment})")
            
            # Notify settings changed
            if self.on_setting_changed:
                self.on_setting_changed('screen_scale', self.current_screen_scale)
                
    def execute_menu_action(self, action):
        """Execute the selected menu action"""
        if action == constants.SETTINGS_MENU_BACK:
            if self.on_back:
                self.on_back()
        elif action == constants.SETTINGS_MENU_POWERUPS:
            # Just toggle powerups
            self.change_setting_value(constants.SETTINGS_MENU_POWERUPS, 0)

    def reset(self):
        """Reset settings screen system"""
        self.settings_menu_selected = constants.SETTINGS_MENU_DIFFICULTY
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        self.value_change_pressed = False