from utils.constants import *

class PlayerCountSystem:
    """Manages player count selection (single vs multiplayer) and multiplayer count selection"""
    
    def __init__(self):
        # Menu selection state
        self.selected_option = 0  # 0 = Single Player, 1 = Multiplayer
        self.in_multiplayer_selection = False  # If true, selecting 2/3/4 players
        self.selected_multiplayer_count = 0  # 0 = 2 players, 1 = 3 players, 2 = 4 players
        
        # Configuration results
        self.player_count = 1  # Final player count (1-4)
        self.is_single_player = True  # True if single player mode
        
        # Transition debouncing to prevent input bleed-through
        self.transition_frames = 0  # Frames since last state transition
        self.TRANSITION_DEBOUNCE_FRAMES = 15  # Quarter second at 60 FPS
        
        # Single-press detection to prevent holding down confirm key
        self.menu_confirm_pressed = False
        
    def get_selected_option(self):
        """Get the currently selected option index"""
        if self.in_multiplayer_selection:
            return self.selected_multiplayer_count
        return self.selected_option
    
    def get_menu_options(self):
        """Get the current menu options list"""
        if self.in_multiplayer_selection:
            return MULTIPLAYER_COUNT_OPTIONS
        return PLAYER_COUNT_MENU_OPTIONS
    
    def navigate_up(self):
        """Navigate up in the menu"""
        if self.in_multiplayer_selection:
            self.selected_multiplayer_count = max(0, self.selected_multiplayer_count - 1)
        else:
            self.selected_option = max(0, self.selected_option - 1)
    
    def navigate_down(self):
        """Navigate down in the menu"""
        if self.in_multiplayer_selection:
            max_index = len(MULTIPLAYER_COUNT_OPTIONS) - 1
            self.selected_multiplayer_count = min(max_index, self.selected_multiplayer_count + 1)
        else:
            max_index = len(PLAYER_COUNT_MENU_OPTIONS) - 1
            self.selected_option = min(max_index, self.selected_option + 1)
    
    def update(self):
        """Update the system (called each frame)"""
        # Decrement transition debounce counter
        if self.transition_frames > 0:
            self.transition_frames -= 1

    def handle_input(self, input_handler):
        """Handle input with single-press detection"""
        # Check for confirmation input with single-press detection
        if input_handler.is_menu_confirm_pressed():
            if not self.menu_confirm_pressed:
                result = self.select_current_option()
                self.menu_confirm_pressed = True
                return result
        else:
            self.menu_confirm_pressed = False
        
        return None

    def select_current_option(self):
        """Select the currently highlighted option"""
        # Ignore confirm input during transition debounce period
        if self.transition_frames > 0:
            return None
            
        if self.in_multiplayer_selection:
            # Convert multiplayer selection to player count
            if self.selected_multiplayer_count == MULTIPLAYER_2_PLAYERS:
                self.player_count = 2
            elif self.selected_multiplayer_count == MULTIPLAYER_3_PLAYERS:
                self.player_count = 3
            elif self.selected_multiplayer_count == MULTIPLAYER_4_PLAYERS:
                self.player_count = 4
            
            self.is_single_player = False
            return "start_controller_setup"  # Signal to start controller setup
            
        else:
            # Main menu selection
            if self.selected_option == PLAYER_COUNT_SINGLE:
                self.player_count = 1
                self.is_single_player = True
                return "start_single_player"  # Signal to start single player game
            elif self.selected_option == PLAYER_COUNT_MULTI:
                self.in_multiplayer_selection = True
                return "enter_multiplayer_selection"  # Signal to enter multiplayer count selection
        
        return None
    
    def go_back(self):
        """Go back in the menu hierarchy"""
        if self.in_multiplayer_selection:
            self.in_multiplayer_selection = False
            return "back_to_player_count"
        else:
            return "back_to_main_menu"
    
    def get_player_count(self):
        """Get the final selected player count"""
        return self.player_count
    
    def is_single_player_mode(self):
        """Check if single player mode was selected"""
        return self.is_single_player
    
    def get_current_screen_title(self):
        """Get the title for the current screen"""
        if self.in_multiplayer_selection:
            return "SELECT PLAYER COUNT"
        return "SELECT GAME MODE"
    
    def get_selection_description(self):
        """Get description text for current selection"""
        if self.in_multiplayer_selection:
            return "Choose how many human players will participate"
        else:
            if self.selected_option == PLAYER_COUNT_SINGLE:
                return "Play against AI opponents"
            else:
                return "Play with friends using controllers"
    
    def reset(self):
        """Reset the system to initial state"""
        self.selected_option = 0
        self.in_multiplayer_selection = False
        self.selected_multiplayer_count = 0
        self.player_count = 1
        self.is_single_player = True
        # Start transition debounce to prevent immediate input processing
        self.transition_frames = self.TRANSITION_DEBOUNCE_FRAMES
        # Reset single-press detection
        self.menu_confirm_pressed = False
    
    def is_in_multiplayer_selection(self):
        """Check if currently in multiplayer count selection"""
        return self.in_multiplayer_selection