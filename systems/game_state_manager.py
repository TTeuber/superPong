from utils.constants import *

class GameStateManager:
    """Manages game state transitions and state-specific logic coordination"""
    
    def __init__(self):
        # Game state management
        self.current_state = GAME_STATE_START_SCREEN
        self.previous_state = GAME_STATE_START_SCREEN  # Store state before pause
        
    def get_current_state(self):
        """Get the current game state"""
        return self.current_state
        
    def get_previous_state(self):
        """Get the previous game state (before pause)"""
        return self.previous_state
        
    def set_state(self, new_state):
        """Set the game state directly"""
        self.current_state = new_state
        
    def toggle_pause(self):
        """Toggle pause state"""
        if self.current_state == GAME_STATE_PAUSED:
            # Unpause - return to previous state
            self.current_state = self.previous_state
            print("Game resumed")
            return "resumed"
        else:
            # Pause - store current state and switch to paused
            self.previous_state = self.current_state
            self.current_state = GAME_STATE_PAUSED
            print("Game paused")
            return "paused"
            
    def resume_game(self):
        """Resume game from pause"""
        if self.current_state == GAME_STATE_PAUSED:
            self.current_state = self.previous_state
            print("Game resumed")
            
    def enter_aiming_mode(self):
        """Enter aiming mode"""
        self.current_state = GAME_STATE_AIMING
        
    def enter_playing_mode(self):
        """Enter playing mode"""
        self.current_state = GAME_STATE_PLAYING
        
    def enter_start_screen(self):
        """Enter start screen mode"""
        self.current_state = GAME_STATE_START_SCREEN
        
    def enter_settings(self):
        """Enter settings screen mode"""
        self.current_state = GAME_STATE_SETTINGS
        
    def enter_game(self):
        """Enter game from start screen"""
        self.current_state = GAME_STATE_PLAYING
        
    def enter_game_over(self):
        """Enter game over state"""
        self.current_state = GAME_STATE_GAME_OVER
        
    def is_start_screen(self):
        """Check if currently on start screen"""
        return self.current_state == GAME_STATE_START_SCREEN
        
    def is_settings(self):
        """Check if currently on settings screen"""
        return self.current_state == GAME_STATE_SETTINGS
        
    def is_game_over(self):
        """Check if currently on game over screen"""
        return self.current_state == GAME_STATE_GAME_OVER
        
    def is_playing(self):
        """Check if currently in playing mode"""
        return self.current_state == GAME_STATE_PLAYING
        
    def is_aiming(self):
        """Check if currently in aiming mode"""
        return self.current_state == GAME_STATE_AIMING
        
    def is_paused(self):
        """Check if currently paused"""
        return self.current_state == GAME_STATE_PAUSED
        
    def reset(self):
        """Reset state manager to initial state"""
        self.current_state = GAME_STATE_START_SCREEN
        self.previous_state = GAME_STATE_START_SCREEN