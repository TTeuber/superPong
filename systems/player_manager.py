from entities.paddle import Paddle
from systems.ai import AIPlayer
from utils import constants

class PlayerManager:
    """Manages player state, lives, and eliminations"""
    
    def __init__(self, ai_difficulty=0.6, player_config=None):
        # Store AI difficulty for creating AI players
        self.ai_difficulty = ai_difficulty
        
        # Player configuration (which players are human vs AI)
        self.player_config = player_config or self._get_default_config()
        self.active_players = len([p for p in self.player_config if p['active']])
        
        # Game state - lives system (only for active players)
        self.lives = []
        self.alive_players = []
        self.starting_lives = constants.STARTING_LIVES
        
        # Initialize based on configuration
        self.paddles = []
        self.ai_players = []
        self.human_players = []  # Track which player IDs are human
        self.init_game_state()
        self.init_paddles()
        self.init_ai_players()
    
    def _get_default_config(self):
        """Get default player configuration (single player mode)"""
        return [
            {'active': True, 'is_human': True, 'controller_index': None},   # Player 0 - Left (human)
            {'active': True, 'is_human': False, 'controller_index': None},  # Player 1 - Right (AI)
            {'active': True, 'is_human': False, 'controller_index': None},  # Player 2 - Top (AI)
            {'active': True, 'is_human': False, 'controller_index': None}   # Player 3 - Bottom (AI)
        ]
    
    def init_game_state(self):
        """Initialize game state based on player configuration"""
        self.lives = []
        self.alive_players = []
        self.human_players = []
        
        for player_id, config in enumerate(self.player_config):
            if config['active']:
                self.lives.append(constants.STARTING_LIVES)
                self.alive_players.append(True)
                if config['is_human']:
                    self.human_players.append(player_id)
            else:
                self.lives.append(0)
                self.alive_players.append(False)
        
    def init_paddles(self):
        """Initialize paddles for active players"""
        self.paddles = [None, None, None, None]  # Keep array structure for indexing
        
        for player_id, config in enumerate(self.player_config):
            if not config['active']:
                continue
                
            if player_id == 0:  # Left paddle
                paddle_margin = int(constants.PADDLE_MARGIN * constants.SCALE_FACTOR)
                paddle_height = int(constants.PADDLE_HEIGHT * constants.SCALE_FACTOR)
                paddle = Paddle(paddle_margin, constants.SCREEN_HEIGHT // 2 - paddle_height // 2,
                               player_id, 'vertical')
            elif player_id == 1:  # Right paddle
                paddle_margin = int(constants.PADDLE_MARGIN * constants.SCALE_FACTOR)
                paddle_width = int(constants.PADDLE_WIDTH * constants.SCALE_FACTOR)
                paddle_height = int(constants.PADDLE_HEIGHT * constants.SCALE_FACTOR)
                paddle = Paddle(constants.SCREEN_WIDTH - paddle_margin - paddle_width,
                               constants.SCREEN_HEIGHT // 2 - paddle_height // 2, player_id, 'vertical')
            elif player_id == 2:  # Top paddle
                paddle_margin = int(constants.PADDLE_MARGIN * constants.SCALE_FACTOR)
                h_paddle_width = int(constants.H_PADDLE_WIDTH * constants.SCALE_FACTOR)
                paddle = Paddle(constants.SCREEN_WIDTH // 2 - h_paddle_width // 2, paddle_margin,
                               player_id, 'horizontal')
            elif player_id == 3:  # Bottom paddle
                paddle_margin = int(constants.PADDLE_MARGIN * constants.SCALE_FACTOR)
                h_paddle_width = int(constants.H_PADDLE_WIDTH * constants.SCALE_FACTOR)
                h_paddle_height = int(constants.H_PADDLE_HEIGHT * constants.SCALE_FACTOR)
                paddle = Paddle(constants.SCREEN_WIDTH // 2 - h_paddle_width // 2,
                               constants.SCREEN_HEIGHT - paddle_margin - h_paddle_height,
                               player_id, 'horizontal')
            else:
                continue  # Skip invalid player IDs
            
            self.paddles[player_id] = paddle
        
    def init_ai_players(self):
        """Initialize AI players for non-human active players"""
        self.ai_players = []
        
        for player_id, config in enumerate(self.player_config):
            if config['active'] and not config['is_human'] and self.paddles[player_id]:
                ai_player = AIPlayer(self.paddles[player_id], difficulty=self.ai_difficulty)
                self.ai_players.append(ai_player)
                print(f"Created AI player for Player {player_id + 1}")
        
    def get_paddles(self):
        """Get all active paddles (filtering out None values)"""
        return [paddle for paddle in self.paddles if paddle is not None]
    
    def get_paddle(self, player_id):
        """Get paddle for specific player"""
        if 0 <= player_id < len(self.paddles):
            return self.paddles[player_id]
        return None
        
    def get_ai_players(self):
        """Get all AI players"""
        return self.ai_players
    
    def update_player_configuration(self, player_config):
        """Update player configuration and reinitialize"""
        self.player_config = player_config
        self.active_players = len([p for p in self.player_config if p['active']])
        self.init_game_state()
        self.init_paddles()
        self.init_ai_players()
    
    def is_player_human(self, player_id):
        """Check if a player is human"""
        if 0 <= player_id < len(self.player_config):
            return self.player_config[player_id].get('is_human', False)
        return False
    
    def get_human_players(self):
        """Get list of human player IDs"""
        return self.human_players
    
    def get_active_player_count(self):
        """Get number of active players"""
        return self.active_players
        
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
        for ai_player in self.ai_players:
            # Get the player ID from the AI player's paddle
            paddle = ai_player.paddle
            if paddle and paddle.player_id < len(self.alive_players) and self.alive_players[paddle.player_id]:
                ai_player.update(ball)
                
    def update_paddles(self):
        """Update paddles (only for alive players)"""
        for i, paddle in enumerate(self.paddles):
            if paddle is not None and i < len(self.alive_players) and self.alive_players[i]:
                paddle.update()
                
    def reset(self):
        """Reset player manager to initial state"""
        # Reset based on current player configuration
        self.init_game_state()
        
        # Reset paddle positions
        self.init_paddles()
        
        # Reinitialize AI with the new paddles
        self.init_ai_players()