import random
import math
from entities.powerup import PowerUp
from entities.ball import Ball
from utils.constants import *

class PowerUpSystem:
    """Manages power-up spawning, collection, and active effects"""
    
    def __init__(self, settings_system=None):
        self.powerups = []  # Active power-ups in the game
        self.active_effects = []  # Currently active power-up effects
        self.spawn_timer = random.randint(POWERUP_SPAWN_MIN_TIME, POWERUP_SPAWN_MAX_TIME)
        self.next_spawn_position = None
        self.settings_system = settings_system
        
        # Chaos power-up specific properties
        self.decoy_balls = []  # Active decoy balls
        self.wild_bounce_timer = 0  # Timer for next wild bounce
        self.control_scramble_mappings = {}  # Player control remappings
        
    def update(self):
        """Update power-up system"""
        # Update spawn timer
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_powerup()
            
        # Update existing power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            
        # Update decoy balls and remove expired ones
        for decoy_ball in self.decoy_balls[:]:
            decoy_ball.update()
            if decoy_ball.is_expired():
                self.decoy_balls.remove(decoy_ball)
            
        # Update chaos effect timers
        if self.wild_bounce_timer > 0:
            self.wild_bounce_timer -= 1
            
        # Update active effects and remove expired ones
        for effect in self.active_effects[:]:
            if effect['duration'] > 0:  # Only decrement timed effects
                effect['duration'] -= 1
                if effect['duration'] <= 0:
                    self.remove_effect(effect)
                    
    def spawn_powerup(self):
        """Spawn a new power-up"""
        # Get enabled power-up types
        enabled_types = self.get_enabled_powerup_types()
        if not enabled_types:
            # Fallback to classic types if no types enabled
            enabled_types = POWERUP_CLASSIC_TYPES
            
        # Generate truly random position in center area (avoiding edges where paddles are)
        margin = 150  # Keep away from paddle areas
        min_x = margin
        max_x = SCREEN_WIDTH - margin
        min_y = margin
        max_y = SCREEN_HEIGHT - margin
        
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        
        # Choose random power-up type from enabled types
        powerup_type = random.choice(enabled_types)
        
        # Create new power-up with specific type
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.append(powerup)
        
        # Reset spawn timer
        self.spawn_timer = random.randint(POWERUP_SPAWN_MIN_TIME, POWERUP_SPAWN_MAX_TIME)
        
    def get_enabled_powerup_types(self):
        """Get list of enabled power-up types from settings"""
        if self.settings_system:
            return self.settings_system.get_enabled_powerups()
        else:
            # Default to classic types if no settings system
            return POWERUP_CLASSIC_TYPES
        
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
        # Handle instant effects
        if effect_data['type'] == POWERUP_PADDLE_SWAP:
            self.execute_paddle_swap(effect_data['player_id'])
            return  # Don't add to active effects list (instant effect)
        elif effect_data['type'] == POWERUP_DECOY_BALL:
            self.spawn_decoy_ball()
            return  # Don't add to active effects list (instant effect)
        elif effect_data['type'] == POWERUP_CONTROL_SCRAMBLE:
            self.scramble_controls()
            # Add to active effects for duration tracking
        elif effect_data['type'] == POWERUP_WILD_BOUNCE:
            self.initialize_wild_bounce()
            # Add to active effects for duration tracking
            
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
        
    # Strategic Power-up Effects
    def execute_paddle_swap(self, player_id):
        """Execute instant paddle swap effect"""
        # This will be handled by the game system
        # Store swap request for game loop to process
        self.pending_paddle_swap = player_id
        
    def has_ghost_ball(self):
        """Check if ghost ball effect is active"""
        for effect in self.active_effects:
            if effect['type'] == POWERUP_GHOST_BALL:
                return True, effect['player_id']
        return False, -1
        
    def has_magnetize(self, player_id):
        """Check if player has magnetize effect active"""
        for effect in self.active_effects:
            if (effect['player_id'] == player_id and 
                effect['type'] == POWERUP_MAGNETIZE):
                return True
        return False
        
    def get_pending_paddle_swap(self):
        """Get and clear pending paddle swap"""
        if hasattr(self, 'pending_paddle_swap'):
            player_id = self.pending_paddle_swap
            del self.pending_paddle_swap
            return player_id
        return -1
        
    def apply_magnetic_force(self, ball, paddles):
        """Apply magnetic force to ball from magnetized paddles"""
        for effect in self.active_effects:
            if effect['type'] == POWERUP_MAGNETIZE:
                player_id = effect['player_id']
                if player_id < len(paddles):
                    paddle = paddles[player_id]
                    self.apply_magnetism(ball, paddle)
                    
    def apply_magnetism(self, ball, paddle):
        """Apply magnetic force between ball and paddle"""
        # Calculate distance between ball and paddle center
        paddle_center = paddle.get_center()
        dx = paddle_center[0] - ball.x
        dy = paddle_center[1] - ball.y
        distance = (dx * dx + dy * dy) ** 0.5
        
        # Only apply force if within magnetic field radius
        if distance < POWERUP_MAGNETIC_FIELD_RADIUS and distance > 0:
            # Calculate magnetic force (stronger when closer)
            force_strength = POWERUP_MAGNETIC_FORCE * (1.0 - distance / POWERUP_MAGNETIC_FIELD_RADIUS)
            
            # Normalize direction vector
            dx_norm = dx / distance
            dy_norm = dy / distance
            
            # Apply magnetic force to ball velocity
            ball.velocity.x += dx_norm * force_strength
            ball.velocity.y += dy_norm * force_strength
            
    # Chaos Power-up Effects
    def spawn_decoy_ball(self):
        """Spawn a decoy ball that doesn't cause life loss"""
        # Spawn decoy ball near center with random direction
        margin = 100
        x = random.randint(margin, SCREEN_WIDTH - margin)
        y = random.randint(margin, SCREEN_HEIGHT - margin)
        
        decoy_ball = Ball(x, y, is_decoy=True)
        self.decoy_balls.append(decoy_ball)
        
    def initialize_wild_bounce(self):
        """Initialize wild bounce effect"""
        # Set timer for first wild bounce
        self.wild_bounce_timer = random.randint(POWERUP_WILD_BOUNCE_MIN_INTERVAL, POWERUP_WILD_BOUNCE_INTERVAL)
        
    def apply_wild_bounce(self, ball):
        """Apply wild bounce effect to the ball"""
        # Check if it's time for a wild bounce
        if self.wild_bounce_timer <= 0 and self.has_wild_bounce():
            # Apply random direction change
            angle_change = random.uniform(-POWERUP_WILD_BOUNCE_ANGLE_RANGE, POWERUP_WILD_BOUNCE_ANGLE_RANGE)
            angle_radians = math.radians(angle_change)
            
            # Calculate current velocity magnitude
            velocity_magnitude = math.sqrt(ball.velocity.x ** 2 + ball.velocity.y ** 2)
            current_angle = math.atan2(ball.velocity.y, ball.velocity.x)
            
            # Apply angle change
            new_angle = current_angle + angle_radians
            ball.velocity.x = math.cos(new_angle) * velocity_magnitude
            ball.velocity.y = math.sin(new_angle) * velocity_magnitude
            
            # Reset timer for next wild bounce
            self.wild_bounce_timer = random.randint(POWERUP_WILD_BOUNCE_MIN_INTERVAL, POWERUP_WILD_BOUNCE_INTERVAL)
            return True  # Indicates a wild bounce occurred
        return False
        
    def scramble_controls(self):
        """Scramble all player controls"""
        # Create random control mappings for all players (0-3)
        players = [0, 1, 2, 3]
        scrambled_players = players.copy()
        random.shuffle(scrambled_players)
        
        # Create mapping dictionary
        self.control_scramble_mappings = {}
        for i, scrambled_id in enumerate(scrambled_players):
            self.control_scramble_mappings[i] = scrambled_id
            
    def get_scrambled_player_id(self, original_player_id):
        """Get the scrambled player ID for control mapping"""
        if self.has_control_scramble():
            return self.control_scramble_mappings.get(original_player_id, original_player_id)
        return original_player_id
        
    def has_wild_bounce(self):
        """Check if wild bounce effect is active"""
        for effect in self.active_effects:
            if effect['type'] == POWERUP_WILD_BOUNCE:
                return True
        return False
        
    def has_control_scramble(self):
        """Check if control scramble effect is active"""
        for effect in self.active_effects:
            if effect['type'] == POWERUP_CONTROL_SCRAMBLE:
                return True
        return False
        
    def get_decoy_balls(self):
        """Get list of active decoy balls"""
        return self.decoy_balls