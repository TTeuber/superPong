from utils.constants import *

class GameStateManager:
    """Manages game state transitions and state-specific logic coordination"""
    
    def __init__(self):
        # Game state management
        self.current_state = GAME_STATE_PLAYING
        self.previous_state = GAME_STATE_PLAYING  # Store state before pause
        
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
        self.current_state = GAME_STATE_PLAYING
        self.previous_state = GAME_STATE_PLAYING