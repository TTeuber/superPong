import json
import os
from utils.constants import *

class SettingsSystem:
    """Manages game settings with JSON file persistence"""
    
    def __init__(self):
        self.settings_file = "settings.json"
        
        # Default settings
        self.default_settings = {
            'ai_difficulty': DIFFICULTY_VALUES[DIFFICULTY_MEDIUM],  # 0.6
            'sound_enabled': True,
            'controller_sensitivity': CONTROLLER_SENSITIVITY
        }
        
        # Current settings (will be loaded from file or set to defaults)
        self.settings = self.default_settings.copy()
        
        # Load settings on initialization
        self.load_settings()
        
    def get_setting(self, key):
        """Get a setting value"""
        return self.settings.get(key, None)
        
    def set_setting(self, key, value):
        """Set a setting value and save to file"""
        if key in self.default_settings:
            self.settings[key] = value
            self.save_settings()
            print(f"Setting '{key}' updated to: {value}")
        else:
            print(f"Warning: Unknown setting key '{key}'")
            
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            print(f"Settings saved to {self.settings_file}")
        except Exception as e:
            print(f"Error saving settings: {e}")
        
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Validate and merge loaded settings with defaults
                for key, value in loaded_settings.items():
                    if key in self.default_settings:
                        # Validate difficulty value
                        if key == 'ai_difficulty':
                            valid_values = list(DIFFICULTY_VALUES.values())
                            if value in valid_values:
                                self.settings[key] = value
                            else:
                                print(f"Invalid difficulty value {value}, using default")
                        # Validate controller sensitivity
                        elif key == 'controller_sensitivity':
                            if 0.5 <= value <= 2.0:
                                self.settings[key] = value
                            else:
                                print(f"Invalid sensitivity value {value}, using default")
                        # Validate boolean settings
                        elif key == 'sound_enabled':
                            if isinstance(value, bool):
                                self.settings[key] = value
                            else:
                                print(f"Invalid sound setting {value}, using default")
                        else:
                            self.settings[key] = value
                
                print(f"Settings loaded from {self.settings_file}")
            else:
                print(f"No settings file found, using defaults")
                self.save_settings()  # Create settings file with defaults
                
        except Exception as e:
            print(f"Error loading settings: {e}, using defaults")
            self.settings = self.default_settings.copy()
        
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.settings = self.default_settings.copy()
        self.save_settings()
        print("Settings reset to defaults")
        
    def get_difficulty_name(self):
        """Get the human-readable difficulty name for current setting"""
        difficulty_value = self.settings.get('ai_difficulty', DIFFICULTY_VALUES[DIFFICULTY_MEDIUM])
        
        # Find matching difficulty name
        for name, value in DIFFICULTY_VALUES.items():
            if abs(value - difficulty_value) < 0.01:  # Float comparison with tolerance
                return name
        
        return DIFFICULTY_MEDIUM  # Default fallback