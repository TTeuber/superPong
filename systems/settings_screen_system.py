from utils.constants import *

class SettingsScreenSystem:
    """Manages the settings screen with menu navigation and value changes"""
    
    def __init__(self):
        # Menu state
        self.settings_menu_selected = SETTINGS_MENU_DIFFICULTY
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        self.value_change_pressed = False
        
        # Callback functions
        self.on_back = None
        self.on_setting_changed = None
        
        # Current settings values (will be loaded from settings system)
        self.current_difficulty = DIFFICULTY_MEDIUM
        self.current_sound_enabled = True
        self.current_controller_sensitivity = 1.0
        
    def set_callbacks(self, on_back=None, on_setting_changed=None):
        """Set callback functions for menu actions"""
        self.on_back = on_back
        self.on_setting_changed = on_setting_changed
        
    def load_current_settings(self, settings_system):
        """Load current settings from the settings system"""
        if settings_system:
            difficulty_value = settings_system.get_setting('ai_difficulty')
            # Find difficulty name from value
            for name, value in DIFFICULTY_VALUES.items():
                if abs(value - difficulty_value) < 0.01:  # Float comparison
                    self.current_difficulty = name
                    break
            
            self.current_sound_enabled = settings_system.get_setting('sound_enabled')
            self.current_controller_sensitivity = settings_system.get_setting('controller_sensitivity')
        
    def get_selected_option(self):
        """Get the currently selected menu option"""
        return self.settings_menu_selected
        
    def get_current_value(self, option):
        """Get the current value for a settings option"""
        if option == SETTINGS_MENU_DIFFICULTY:
            return self.current_difficulty
        elif option == SETTINGS_MENU_SOUND:
            return "On" if self.current_sound_enabled else "Off"
        elif option == SETTINGS_MENU_CONTROLLER:
            return f"{self.current_controller_sensitivity:.1f}"
        return ""
        
    def handle_settings_input(self, input_handler):
        """Handle input for settings menu navigation"""
        # Check for menu navigation (up/down)
        nav_direction = input_handler.get_menu_navigation()
        if nav_direction != 0:
            if not self.menu_nav_pressed:
                # Navigate menu
                self.settings_menu_selected = (self.settings_menu_selected + nav_direction) % len(SETTINGS_MENU_OPTIONS)
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
            
        # Check for confirmation input (for Back option)
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
        if setting_option == SETTINGS_MENU_DIFFICULTY:
            current_index = DIFFICULTY_OPTIONS.index(self.current_difficulty)
            new_index = (current_index + direction) % len(DIFFICULTY_OPTIONS)
            self.current_difficulty = DIFFICULTY_OPTIONS[new_index]
            
            # Notify settings changed
            if self.on_setting_changed:
                self.on_setting_changed('ai_difficulty', DIFFICULTY_VALUES[self.current_difficulty])
                
        elif setting_option == SETTINGS_MENU_SOUND:
            self.current_sound_enabled = not self.current_sound_enabled
            
            # Notify settings changed
            if self.on_setting_changed:
                self.on_setting_changed('sound_enabled', self.current_sound_enabled)
                
        elif setting_option == SETTINGS_MENU_CONTROLLER:
            # Change sensitivity in 0.1 increments between 0.5 and 2.0
            sensitivity_step = 0.1 * direction
            new_sensitivity = self.current_controller_sensitivity + sensitivity_step
            new_sensitivity = max(0.5, min(2.0, new_sensitivity))  # Clamp between 0.5 and 2.0
            self.current_controller_sensitivity = round(new_sensitivity, 1)
            
            # Notify settings changed
            if self.on_setting_changed:
                self.on_setting_changed('controller_sensitivity', self.current_controller_sensitivity)
                
    def execute_menu_action(self, action):
        """Execute the selected menu action"""
        if action == SETTINGS_MENU_BACK:
            if self.on_back:
                self.on_back()
                
    def reset(self):
        """Reset settings screen system"""
        self.settings_menu_selected = SETTINGS_MENU_DIFFICULTY
        self.menu_nav_pressed = False
        self.menu_confirm_pressed = False
        self.value_change_pressed = False