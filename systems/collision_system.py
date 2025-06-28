from utils.constants import *

class CollisionSystem:
    """Manages all collision detection and handling"""
    
    def __init__(self):
        pass
        
    def check_ball_paddle_collisions(self, ball, paddles, alive_players, particle_system, renderer):
        """Check and handle ball-paddle collisions"""
        for i, paddle in enumerate(paddles):
            if alive_players[i] and ball.rect.colliderect(paddle.rect):
                ball.bounce_off_paddle(paddle)
                # Add particle effect for paddle hit
                particle_system.add_ball_impact_burst(ball.x, ball.y, paddle.color)
                # Add screen shake for paddle hit
                renderer.add_screen_shake(3, 8)
                return True  # Collision occurred
        return False  # No collision
        
    def check_ball_boundary_collisions(self, ball, alive_players, particle_system, renderer):
        """Check ball boundary collisions - return collision info"""
        collision_info = {
            'collision_occurred': False,
            'player_hit': -1,
            'bounced': False,
            'life_lost': False
        }
        
        # Check left boundary
        if ball.x <= BOUNDARY_THICKNESS:
            collision_info['collision_occurred'] = True
            collision_info['player_hit'] = 0
            if alive_players[0]:  # Live player - loses life
                collision_info['life_lost'] = True
            else:  # Dead player - ball bounces
                ball.bounce_off_wall("left")
                particle_system.add_wall_impact_sparks(ball.x, ball.y)
                renderer.add_screen_shake(1, 4)
                collision_info['bounced'] = True

        # Check right boundary
        elif ball.x >= SCREEN_WIDTH - BOUNDARY_THICKNESS:
            collision_info['collision_occurred'] = True
            collision_info['player_hit'] = 1
            if alive_players[1]:  # Live player - loses life
                collision_info['life_lost'] = True
            else:  # Dead player - ball bounces
                ball.bounce_off_wall("right")
                particle_system.add_wall_impact_sparks(ball.x, ball.y)
                renderer.add_screen_shake(1, 4)
                collision_info['bounced'] = True

        # Check top boundary
        elif ball.y <= BOUNDARY_THICKNESS:
            collision_info['collision_occurred'] = True
            collision_info['player_hit'] = 2
            if alive_players[2]:  # Live player - loses life
                collision_info['life_lost'] = True
            else:  # Dead player - ball bounces
                ball.bounce_off_wall("top")
                particle_system.add_wall_impact_sparks(ball.x, ball.y)
                renderer.add_screen_shake(1, 4)
                collision_info['bounced'] = True

        # Check bottom boundary
        elif ball.y >= SCREEN_HEIGHT - BOUNDARY_THICKNESS:
            collision_info['collision_occurred'] = True
            collision_info['player_hit'] = 3
            if alive_players[3]:  # Live player - loses life
                collision_info['life_lost'] = True
            else:  # Dead player - ball bounces
                ball.bounce_off_wall("bottom")
                particle_system.add_wall_impact_sparks(ball.x, ball.y)
                renderer.add_screen_shake(1, 4)
                collision_info['bounced'] = True
                
        return collision_info