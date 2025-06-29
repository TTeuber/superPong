from utils.math_utils import clamp
from utils.constants import (AI_PREDICTION_ENABLED, AI_PREDICTION_LOOKAHEAD_TIME, AI_MAX_PREDICTION_BOUNCES, 
                             AI_PREDICTION_ACCURACY, AI_CENTER_SEEK_ENABLED, AI_CENTER_SEEK_STRENGTH, 
                             AI_ANTICIPATION_DISTANCE, AI_DEFENSIVE_ZONE_SIZE, AI_MIN_THREAT_DISTANCE,
                             AI_OPPOSITE_WALL_THRESHOLD, SCREEN_WIDTH, SCREEN_HEIGHT, BOUNDARY_THICKNESS)
import math

class AIPlayer:
    def __init__(self, paddle, difficulty=0.8):
        self.paddle = paddle
        self.difficulty = difficulty  # 0.0 to 1.0, higher = better AI
        self.reaction_delay = 0
        self.max_reaction_delay = int(10 * (1 - difficulty))  # Frames to delay reaction
        self.target_position = None
        self.movement_smoothing = 0.3  # Base smoothing increased from 0.15 to 0.3
        
        # Prediction stabilization
        self.prediction_history = []
        self.max_prediction_history = 5
        
        # Movement hysteresis
        self.is_moving = False
        self.movement_commitment_frames = 0
        self.min_movement_duration = 3  # Minimum frames to continue movement
        
        # Threshold hysteresis
        self.last_threshold_state = "normal"  # "tight", "normal", "loose"

    def predict_ball_intersection(self, ball):
        """Predict where the ball will intersect with this paddle's plane"""
        if not AI_PREDICTION_ENABLED:
            return ball.x, ball.y
        
        # Get current ball state
        ball_x, ball_y = ball.x, ball.y
        vel_x, vel_y = ball.velocity.x, ball.velocity.y
        
        # Determine the plane this paddle defends
        if self.paddle.orientation == 'vertical':
            # Vertical paddle defends a vertical line
            if self.paddle.x < SCREEN_WIDTH // 2:  # Left paddle
                target_x = self.paddle.x + self.paddle.width
            else:  # Right paddle
                target_x = self.paddle.x
            
            # Calculate time to reach paddle's X position
            if abs(vel_x) < 0.1:  # Ball not moving horizontally
                return ball_x, ball_y
            
            time_to_reach = (target_x - ball_x) / vel_x
            
            # If ball is moving away from paddle, return current position
            if time_to_reach < 0:
                return ball_x, ball_y
            
            # Predict Y position at intersection
            predicted_y = ball_y + vel_y * time_to_reach
            
            # Account for wall bounces
            predicted_y = self._predict_wall_bounces_y(predicted_y, vel_y, time_to_reach)
            
            return target_x, predicted_y
            
        else:  # Horizontal paddle
            # Horizontal paddle defends a horizontal line
            if self.paddle.y < SCREEN_HEIGHT // 2:  # Top paddle
                target_y = self.paddle.y + self.paddle.height
            else:  # Bottom paddle
                target_y = self.paddle.y
            
            # Calculate time to reach paddle's Y position
            if abs(vel_y) < 0.1:  # Ball not moving vertically
                return ball_x, ball_y
            
            time_to_reach = (target_y - ball_y) / vel_y
            
            # If ball is moving away from paddle, return current position
            if time_to_reach < 0:
                return ball_x, ball_y
            
            # Predict X position at intersection
            predicted_x = ball_x + vel_x * time_to_reach
            
            # Account for wall bounces
            predicted_x = self._predict_wall_bounces_x(predicted_x, vel_x, time_to_reach)
            
            return predicted_x, target_y
    
    def _predict_wall_bounces_y(self, predicted_y, vel_y, time_remaining):
        """Predict Y position accounting for wall bounces"""
        if AI_MAX_PREDICTION_BOUNCES == 0:
            return predicted_y
        
        # Check if ball will hit top or bottom wall
        if predicted_y < BOUNDARY_THICKNESS:
            # Ball hits top wall
            bounce_time = (BOUNDARY_THICKNESS - predicted_y) / abs(vel_y) if vel_y < 0 else 0
            if bounce_time < time_remaining:
                # Ball bounces off top wall
                remaining_time = time_remaining - bounce_time
                new_vel_y = -vel_y  # Reverse Y velocity
                return BOUNDARY_THICKNESS + new_vel_y * remaining_time
        
        elif predicted_y > SCREEN_HEIGHT - BOUNDARY_THICKNESS:
            # Ball hits bottom wall
            bounce_time = (predicted_y - (SCREEN_HEIGHT - BOUNDARY_THICKNESS)) / abs(vel_y) if vel_y > 0 else 0
            if bounce_time < time_remaining:
                # Ball bounces off bottom wall
                remaining_time = time_remaining - bounce_time
                new_vel_y = -vel_y  # Reverse Y velocity
                return (SCREEN_HEIGHT - BOUNDARY_THICKNESS) + new_vel_y * remaining_time
        
        return predicted_y
    
    def _predict_wall_bounces_x(self, predicted_x, vel_x, time_remaining):
        """Predict X position accounting for wall bounces"""
        if AI_MAX_PREDICTION_BOUNCES == 0:
            return predicted_x
        
        # Check if ball will hit left or right wall
        if predicted_x < BOUNDARY_THICKNESS:
            # Ball hits left wall
            bounce_time = (BOUNDARY_THICKNESS - predicted_x) / abs(vel_x) if vel_x < 0 else 0
            if bounce_time < time_remaining:
                # Ball bounces off left wall
                remaining_time = time_remaining - bounce_time
                new_vel_x = -vel_x  # Reverse X velocity
                return BOUNDARY_THICKNESS + new_vel_x * remaining_time
        
        elif predicted_x > SCREEN_WIDTH - BOUNDARY_THICKNESS:
            # Ball hits right wall
            bounce_time = (predicted_x - (SCREEN_WIDTH - BOUNDARY_THICKNESS)) / abs(vel_x) if vel_x > 0 else 0
            if bounce_time < time_remaining:
                # Ball bounces off right wall
                remaining_time = time_remaining - bounce_time
                new_vel_x = -vel_x  # Reverse X velocity
                return (SCREEN_WIDTH - BOUNDARY_THICKNESS) + new_vel_x * remaining_time
        
        return predicted_x

    def stabilize_prediction(self, predicted_x, predicted_y):
        """Stabilize predictions by averaging recent history"""
        # Add current prediction to history
        self.prediction_history.append((predicted_x, predicted_y))
        if len(self.prediction_history) > self.max_prediction_history:
            self.prediction_history.pop(0)
        
        # Return average of recent predictions for stability
        if len(self.prediction_history) >= 2:
            avg_x = sum(p[0] for p in self.prediction_history) / len(self.prediction_history)
            avg_y = sum(p[1] for p in self.prediction_history) / len(self.prediction_history)
            
            # Blend current prediction with historical average for stability
            blend_factor = 0.4  # How much to blend with history
            stable_x = predicted_x * (1 - blend_factor) + avg_x * blend_factor
            stable_y = predicted_y * (1 - blend_factor) + avg_y * blend_factor
            return stable_x, stable_y
        
        return predicted_x, predicted_y

    def get_dynamic_smoothing(self, ball):
        """Calculate dynamic smoothing factor based on ball distance"""
        ball_distance = self.calculate_ball_distance(ball)
        
        # Increase smoothing when ball is close to reduce shaking
        if ball_distance < AI_ANTICIPATION_DISTANCE:
            # Very close: much higher smoothing
            distance_factor = ball_distance / AI_ANTICIPATION_DISTANCE
            extra_smoothing = (1 - distance_factor) * 0.3  # Up to 0.3 extra smoothing
            return min(self.movement_smoothing + extra_smoothing, 0.8)  # Cap at 0.8
        
        return self.movement_smoothing

    def get_stable_threshold(self, ball):
        """Calculate movement threshold with hysteresis to prevent rapid switching"""
        ball_distance = self.calculate_ball_distance(ball)
        is_approaching = self.is_ball_approaching(ball)
        base_threshold = 35 * (1 - self.difficulty + 0.3)
        
        # Determine what threshold state we should be in
        if ball_distance < AI_ANTICIPATION_DISTANCE * 0.8 and is_approaching:
            target_state = "tight"
        elif ball_distance > AI_ANTICIPATION_DISTANCE * 1.3 or not is_approaching:
            target_state = "loose"
        else:
            target_state = "normal"
        
        # Apply hysteresis - only change state if significantly different
        if self.last_threshold_state != target_state:
            # Only change if we're moving to a clearly different state
            if (self.last_threshold_state == "tight" and target_state == "loose") or \
               (self.last_threshold_state == "loose" and target_state == "tight") or \
               (self.last_threshold_state == "normal" and target_state != "normal"):
                self.last_threshold_state = target_state
        
        # Return threshold based on stable state
        if self.last_threshold_state == "tight":
            return base_threshold * 0.8  # Tighter than before
        elif self.last_threshold_state == "loose":
            return base_threshold * 1.3  # Looser than before
        else:
            return base_threshold  # Normal

    def get_paddle_center_position(self):
        """Get the ideal center position for this paddle"""
        if self.paddle.orientation == 'vertical':
            return SCREEN_HEIGHT // 2
        else:
            return SCREEN_WIDTH // 2
    
    def calculate_ball_distance(self, ball):
        """Calculate distance from ball to paddle"""
        paddle_center = self.paddle.get_center()
        return math.sqrt((ball.x - paddle_center[0])**2 + (ball.y - paddle_center[1])**2)
    
    def is_ball_approaching(self, ball):
        """Determine if ball is moving toward this paddle"""
        if self.paddle.orientation == 'vertical':
            if self.paddle.x < SCREEN_WIDTH // 2:  # Left paddle
                return ball.velocity.x < 0
            else:  # Right paddle
                return ball.velocity.x > 0
        else:  # Horizontal paddle
            if self.paddle.y < SCREEN_HEIGHT // 2:  # Top paddle
                return ball.velocity.y < 0
            else:  # Bottom paddle
                return ball.velocity.y > 0
    
    def is_ball_heading_to_opposite_wall(self, ball):
        """Determine if ball is clearly heading toward the opposite wall (not this paddle's responsibility)"""
        if self.paddle.orientation == 'vertical':
            if self.paddle.x < SCREEN_WIDTH // 2:  # Left paddle
                # Ball heading strongly right (toward right wall)
                return ball.velocity.x > AI_OPPOSITE_WALL_THRESHOLD * abs(ball.velocity.y)
            else:  # Right paddle
                # Ball heading strongly left (toward left wall)  
                return ball.velocity.x < -AI_OPPOSITE_WALL_THRESHOLD * abs(ball.velocity.y)
        else:  # Horizontal paddle
            if self.paddle.y < SCREEN_HEIGHT // 2:  # Top paddle
                # Ball heading strongly down (toward bottom wall)
                return ball.velocity.y > AI_OPPOSITE_WALL_THRESHOLD * abs(ball.velocity.x)
            else:  # Bottom paddle
                # Ball heading strongly up (toward top wall)
                return ball.velocity.y < -AI_OPPOSITE_WALL_THRESHOLD * abs(ball.velocity.x)
    
    def calculate_strategic_target(self, ball, predicted_x, predicted_y):
        """Calculate target position considering strategic positioning"""
        if not AI_CENTER_SEEK_ENABLED:
            return predicted_x, predicted_y
        
        # Calculate distance to ball and whether it's approaching
        ball_distance = self.calculate_ball_distance(ball)
        is_approaching = self.is_ball_approaching(ball)
        is_heading_opposite = self.is_ball_heading_to_opposite_wall(ball)
        
        # Get ideal center position
        center_position = self.get_paddle_center_position()
        
        # Determine positioning strategy
        if self.paddle.orientation == 'vertical':
            current_target = predicted_y
            
            # Strong center-seeking if ball is heading to opposite wall
            if is_heading_opposite:
                center_blend = AI_CENTER_SEEK_STRENGTH * 1.2  # Extra strong center-seeking
                strategic_target = current_target * (1 - center_blend) + center_position * center_blend
                return predicted_x, strategic_target
            
            # If ball is far away or moving away, blend toward center
            elif ball_distance > AI_MIN_THREAT_DISTANCE or not is_approaching:
                center_blend = AI_CENTER_SEEK_STRENGTH * (1 - self.difficulty * 0.3)
                strategic_target = current_target * (1 - center_blend) + center_position * center_blend
                return predicted_x, strategic_target
            
            # If ball is close and approaching, prioritize interception but allow some center bias
            elif ball_distance < AI_ANTICIPATION_DISTANCE and is_approaching:
                # Use predicted position but with slight center bias for better positioning
                center_blend = AI_CENTER_SEEK_STRENGTH * 0.2  # Light center bias
                strategic_target = current_target * (1 - center_blend) + center_position * center_blend
                return predicted_x, strategic_target
            
        else:  # Horizontal paddle
            current_target = predicted_x
            
            # Strong center-seeking if ball is heading to opposite wall
            if is_heading_opposite:
                center_blend = AI_CENTER_SEEK_STRENGTH * 1.2  # Extra strong center-seeking
                strategic_target = current_target * (1 - center_blend) + center_position * center_blend
                return strategic_target, predicted_y
            
            # If ball is far away or moving away, blend toward center
            elif ball_distance > AI_MIN_THREAT_DISTANCE or not is_approaching:
                center_blend = AI_CENTER_SEEK_STRENGTH * (1 - self.difficulty * 0.3)
                strategic_target = current_target * (1 - center_blend) + center_position * center_blend
                return strategic_target, predicted_y
            
            # If ball is close and approaching, prioritize interception but allow some center bias
            elif ball_distance < AI_ANTICIPATION_DISTANCE and is_approaching:
                # Use predicted position but with slight center bias for better positioning
                center_blend = AI_CENTER_SEEK_STRENGTH * 0.2  # Light center bias
                strategic_target = current_target * (1 - center_blend) + center_position * center_blend
                return strategic_target, predicted_y
        
        # Default: use predicted position
        return predicted_x, predicted_y

    def update(self, ball):
        """Update AI paddle movement to track the ball"""
        # Simple reaction delay to make AI beatable
        if self.reaction_delay > 0:
            self.reaction_delay -= 1
            return

        paddle_center = self.paddle.get_center()
        
        # Get predicted ball intersection point
        predicted_x, predicted_y = self.predict_ball_intersection(ball)
        
        # Stabilize predictions to reduce shaking
        stable_x, stable_y = self.stabilize_prediction(predicted_x, predicted_y)
        
        # Apply strategic positioning
        strategic_x, strategic_y = self.calculate_strategic_target(ball, stable_x, stable_y)

        # Calculate desired position with smoothing
        if self.paddle.orientation == 'vertical':
            # Vertical paddle follows strategic Y position
            ball_target = strategic_y
            
            # Smooth target position update with dynamic smoothing
            dynamic_smoothing = self.get_dynamic_smoothing(ball)
            if self.target_position is None:
                self.target_position = ball_target
            else:
                self.target_position += (ball_target - self.target_position) * dynamic_smoothing
            
            current_y = paddle_center[1]
            
            # Reset movement flags
            self.paddle.moving_up = False
            self.paddle.moving_down = False

            # Move towards smoothed target with stable threshold and movement hysteresis
            diff = self.target_position - current_y
            threshold = self.get_stable_threshold(ball)
            
            # Movement commitment - continue current movement for minimum duration
            if self.movement_commitment_frames > 0:
                self.movement_commitment_frames -= 1
                # Continue current movement, don't change direction
            elif abs(diff) > threshold:
                if diff < 0:
                    self.paddle.moving_up = True
                    self.is_moving = True
                else:
                    self.paddle.moving_down = True
                    self.is_moving = True

                # Start movement commitment to prevent rapid changes
                self.movement_commitment_frames = self.min_movement_duration
                
                # Add reaction delay only for significant movements
                if abs(diff) > threshold * 1.5:  # Only delay for large movements
                    self.reaction_delay = self.max_reaction_delay
            else:
                self.is_moving = False

        else:  # horizontal paddle
            # Horizontal paddle follows strategic X position
            ball_target = strategic_x
            
            # Smooth target position update with dynamic smoothing
            dynamic_smoothing = self.get_dynamic_smoothing(ball)
            if self.target_position is None:
                self.target_position = ball_target
            else:
                self.target_position += (ball_target - self.target_position) * dynamic_smoothing
            
            current_x = paddle_center[0]
            
            # Reset movement flags
            self.paddle.moving_left = False
            self.paddle.moving_right = False

            # Move towards smoothed target with stable threshold and movement hysteresis
            diff = self.target_position - current_x
            threshold = self.get_stable_threshold(ball)
            
            # Movement commitment - continue current movement for minimum duration
            if self.movement_commitment_frames > 0:
                self.movement_commitment_frames -= 1
                # Continue current movement, don't change direction
            elif abs(diff) > threshold:
                if diff < 0:
                    self.paddle.moving_left = True
                    self.is_moving = True
                else:
                    self.paddle.moving_right = True
                    self.is_moving = True

                # Start movement commitment to prevent rapid changes
                self.movement_commitment_frames = self.min_movement_duration
                
                # Add reaction delay only for significant movements
                if abs(diff) > threshold * 1.5:  # Only delay for large movements
                    self.reaction_delay = self.max_reaction_delay
            else:
                self.is_moving = False