from utils.math_utils import clamp

class AIPlayer:
    def __init__(self, paddle, difficulty=0.8):
        self.paddle = paddle
        self.difficulty = difficulty  # 0.0 to 1.0, higher = better AI
        self.reaction_delay = 0
        self.max_reaction_delay = int(10 * (1 - difficulty))  # Frames to delay reaction
        self.target_position = None
        self.movement_smoothing = 0.15  # How quickly AI adjusts to new target (0.1 = slow, 1.0 = instant)

    def update(self, ball):
        """Update AI paddle movement to track the ball"""
        # Simple reaction delay to make AI beatable
        if self.reaction_delay > 0:
            self.reaction_delay -= 1
            return

        paddle_center = self.paddle.get_center()

        # Calculate desired position with smoothing
        if self.paddle.orientation == 'vertical':
            # Vertical paddle follows ball's Y position
            ball_target = ball.y
            
            # Smooth target position update
            if self.target_position is None:
                self.target_position = ball_target
            else:
                self.target_position += (ball_target - self.target_position) * self.movement_smoothing
            
            current_y = paddle_center[1]
            
            # Reset movement flags
            self.paddle.moving_up = False
            self.paddle.moving_down = False

            # Move towards smoothed target with larger dead zone
            diff = self.target_position - current_y
            threshold = 35 * (1 - self.difficulty + 0.3)  # Larger dead zone to reduce jitter

            if abs(diff) > threshold:
                if diff < 0:
                    self.paddle.moving_up = True
                else:
                    self.paddle.moving_down = True

                # Add reaction delay after movement decision
                self.reaction_delay = self.max_reaction_delay

        else:  # horizontal paddle
            # Horizontal paddle follows ball's X position
            ball_target = ball.x
            
            # Smooth target position update
            if self.target_position is None:
                self.target_position = ball_target
            else:
                self.target_position += (ball_target - self.target_position) * self.movement_smoothing
            
            current_x = paddle_center[0]
            
            # Reset movement flags
            self.paddle.moving_left = False
            self.paddle.moving_right = False

            # Move towards smoothed target with larger dead zone
            diff = self.target_position - current_x
            threshold = 35 * (1 - self.difficulty + 0.3)  # Larger dead zone to reduce jitter

            if abs(diff) > threshold:
                if diff < 0:
                    self.paddle.moving_left = True
                else:
                    self.paddle.moving_right = True

                # Add reaction delay after movement decision
                self.reaction_delay = self.max_reaction_delay