from entities.paddle import Paddle
from systems.ai import AIPlayer
from utils.constants import *

class PlayerManager:
    """Manages player state, lives, and eliminations"""
    
    def __init__(self):
        # Game state - lives system
        self.lives = [5, 5, 5, 5]  # Each player starts with 5 lives
        self.alive_players = [True, True, True, True]  # Track which players are still alive
        self.starting_lives = 5
        
        # Initialize paddles and AI
        self.paddles = []
        self.ai_players = []
        self.init_paddles()
        self.init_ai_players()
        
    def init_paddles(self):
        """Initialize the four paddles"""
        self.paddles = []

        # Player 1 - Left paddle (human player)
        left_paddle = Paddle(PADDLE_MARGIN, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                             0, 'vertical')
        self.paddles.append(left_paddle)

        # Player 2 - Right paddle (AI)
        right_paddle = Paddle(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
                              SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, 1, 'vertical')
        self.paddles.append(right_paddle)

        # Player 3 - Top paddle (AI)
        top_paddle = Paddle(SCREEN_WIDTH // 2 - H_PADDLE_WIDTH // 2, PADDLE_MARGIN,
                            2, 'horizontal')
        self.paddles.append(top_paddle)

        # Player 4 - Bottom paddle (AI)
        bottom_paddle = Paddle(SCREEN_WIDTH // 2 - H_PADDLE_WIDTH // 2,
                               SCREEN_HEIGHT - PADDLE_MARGIN - H_PADDLE_HEIGHT,
                               3, 'horizontal')
        self.paddles.append(bottom_paddle)
        
    def init_ai_players(self):
        """Initialize AI players (players 1, 2, 3 are AI by default)"""
        self.ai_players = [
            AIPlayer(self.paddles[1], difficulty=0.7),  # Player 2 (right)
            AIPlayer(self.paddles[2], difficulty=0.6),  # Player 3 (top)
            AIPlayer(self.paddles[3], difficulty=0.6),  # Player 4 (bottom)
        ]
        
    def get_paddles(self):
        """Get all paddles"""
        return self.paddles
        
    def get_ai_players(self):
        """Get all AI players"""
        return self.ai_players
        
    def get_lives(self):
        """Get lives array"""
        return self.lives
        
    def get_alive_players(self):
        """Get alive players array"""
        return self.alive_players
        
    def is_player_alive(self, player_id):
        """Check if a specific player is alive"""
        return self.alive_players[player_id]
        
    def get_alive_count(self):
        """Get the number of alive players"""
        return sum(self.alive_players)
        
    def lose_life(self, player_id):
        """Player loses a life and returns elimination info"""
        if player_id < 0 or player_id >= 4:
            return {'eliminated': False, 'game_over': False, 'winner': -1}
            
        self.lives[player_id] -= 1
        
        result = {
            'eliminated': False,
            'game_over': False,
            'winner': -1
        }
        
        # Check if player is eliminated
        if self.lives[player_id] <= 0:
            self.alive_players[player_id] = False
            result['eliminated'] = True
            print(f"Player {player_id + 1} eliminated!")
            
            # Check for game over (only one player left)
            alive_count = sum(self.alive_players)
            if alive_count <= 1:
                result['game_over'] = True
                # Find the winner
                for i, alive in enumerate(self.alive_players):
                    if alive:
                        result['winner'] = i
                        break
                        
        return result
        
    def get_winner_info(self):
        """Get information about the game winner"""
        winner = -1
        for i, alive in enumerate(self.alive_players):
            if alive:
                winner = i
                break
        
        if winner >= 0:
            return {
                'winner': winner,
                'lives_remaining': self.lives[winner],
                'message': f"Player {winner + 1} wins! Last player standing with {self.lives[winner]} lives remaining!"
            }
        else:
            return {
                'winner': -1,
                'lives_remaining': 0,
                'message': "Game over - all players eliminated!"
            }
            
    def update_ai_players(self, ball):
        """Update AI players (only for alive players)"""
        for i, ai_player in enumerate(self.ai_players):
            # AI players are at indices 1, 2, 3 (not 0 since player 0 is human)
            ai_player_index = i + 1
            if self.alive_players[ai_player_index]:
                ai_player.update(ball)
                
    def update_paddles(self):
        """Update paddles (only for alive players)"""
        for i, paddle in enumerate(self.paddles):
            if self.alive_players[i]:
                paddle.update()
                
    def reset(self):
        """Reset player manager to initial state"""
        self.lives = [5, 5, 5, 5]
        self.alive_players = [True, True, True, True]
        
        # Reset paddle positions
        self.init_paddles()
        
        # Reinitialize AI with the new paddles
        self.init_ai_players()