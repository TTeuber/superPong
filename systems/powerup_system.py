import random
from entities.powerup import PowerUp
from utils.constants import *

class PowerUpSystem:
    """Manages power-up spawning, collection, and active effects"""
    
    def __init__(self):
        self.powerups = []  # Active power-ups in the game
        self.active_effects = []  # Currently active power-up effects
        self.spawn_timer = random.randint(POWERUP_SPAWN_MIN_TIME, POWERUP_SPAWN_MAX_TIME)
        self.next_spawn_position = None
        
    def update(self):
        """Update power-up system"""
        # Update spawn timer
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_powerup()
            
        # Update existing power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            
        # Update active effects and remove expired ones
        for effect in self.active_effects[:]:
            if effect['duration'] > 0:  # Only decrement timed effects
                effect['duration'] -= 1
                if effect['duration'] <= 0:
                    self.remove_effect(effect)
                    
    def spawn_powerup(self):
        """Spawn a new power-up"""
        # Generate truly random position in center area (avoiding edges where paddles are)
        margin = 150  # Keep away from paddle areas
        min_x = margin
        max_x = SCREEN_WIDTH - margin
        min_y = margin
        max_y = SCREEN_HEIGHT - margin
        
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        
        # Create new power-up
        powerup = PowerUp(x, y)
        self.powerups.append(powerup)
        
        # Reset spawn timer
        self.spawn_timer = random.randint(POWERUP_SPAWN_MIN_TIME, POWERUP_SPAWN_MAX_TIME)
        
    def check_ball_collection(self, ball, alive_players):
        """Check if ball collected a power-up"""
        for powerup in self.powerups[:]:
            if not powerup.can_collect():
                continue
                
            # Check collision using distance between ball and power-up
            distance = ((ball.x - powerup.x) ** 2 + (ball.y - powerup.y) ** 2) ** 0.5
            if distance <= POWERUP_COLLECT_RADIUS:
                # Get the player who last hit the ball
                player_id = ball.last_hit_player_id
                
                # Validate player ID and make sure they're alive
                if player_id >= 0 and player_id < len(alive_players) and alive_players[player_id]:
                    # Collect the power-up
                    effect_data = powerup.collect(player_id)
                    self.apply_effect(effect_data)
                    self.powerups.remove(powerup)
                    return effect_data  # Return for particle effects
                    
        return None
        
    def check_collection(self, paddles, alive_players):
        """Legacy method - kept for compatibility but should use check_ball_collection"""
        # This method is deprecated but kept to avoid breaking existing code
        return None
        
    def apply_effect(self, effect_data):
        """Apply a power-up effect"""
        # Check if player already has this type of effect
        for existing in self.active_effects:
            if (existing['player_id'] == effect_data['player_id'] and 
                existing['type'] == effect_data['type']):
                # Refresh duration
                existing['duration'] = effect_data['duration']
                return
                
        # Add new effect
        self.active_effects.append(effect_data)
        
    def remove_effect(self, effect):
        """Remove an expired effect"""
        if effect in self.active_effects:
            self.active_effects.remove(effect)
            
    def get_player_effects(self, player_id):
        """Get all active effects for a specific player"""
        return [e for e in self.active_effects if e['player_id'] == player_id]
        
    def has_shield(self, player_id):
        """Check if player has an active shield"""
        for effect in self.active_effects:
            if (effect['player_id'] == player_id and 
                effect['type'] == POWERUP_SHIELD):
                return True
        return False
        
    def use_shield(self, player_id):
        """Use up a player's shield"""
        for effect in self.active_effects[:]:
            if (effect['player_id'] == player_id and 
                effect['type'] == POWERUP_SHIELD):
                self.active_effects.remove(effect)
                return True
        return False
        
    def get_paddle_size_modifier(self, player_id, all_player_ids):
        """Get the paddle size modifier for a player"""
        modifier = 1.0
        
        for effect in self.active_effects:
            if effect['type'] == POWERUP_PADDLE_SIZE:
                if effect['variant'] == "increase_self" and effect['player_id'] == player_id:
                    modifier *= POWERUP_PADDLE_SIZE_INCREASE
                elif effect['variant'] == "decrease_enemies" and effect['player_id'] != player_id:
                    # Only apply if the effect owner is the one checking
                    for pid in all_player_ids:
                        if pid == effect['player_id']:
                            continue
                        if pid == player_id:
                            modifier *= POWERUP_PADDLE_SIZE_DECREASE
                            
        return modifier
        
    def get_ball_speed_modifier(self):
        """Get the current ball speed modifier"""
        modifier = 1.0
        
        # Find the most recent ball speed effect
        for effect in reversed(self.active_effects):
            if effect['type'] == POWERUP_BALL_SPEED:
                if effect['variant'] == "slow":
                    return POWERUP_BALL_SPEED_SLOW
                elif effect['variant'] == "fast":
                    return POWERUP_BALL_SPEED_FAST
                    
        return modifier
        
    def clear(self):
        """Clear all power-ups and effects"""
        self.powerups.clear()
        self.active_effects.clear()
        self.spawn_timer = random.randint(POWERUP_SPAWN_MIN_TIME, POWERUP_SPAWN_MAX_TIME)
        
    def get_powerups(self):
        """Get list of active power-ups"""
        return self.powerups
        
    def get_active_effects(self):
        """Get list of active effects"""
        return self.active_effects