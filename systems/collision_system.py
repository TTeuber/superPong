from utils.constants import *

class CollisionSystem:
    """Manages all collision detection and handling"""
    
    def __init__(self):
        self.powerup_system = None  # Will be set from game.py
        
    def set_powerup_system(self, powerup_system):
        """Set reference to power-up system for shield checks"""
        self.powerup_system = powerup_system
        
    def check_ball_paddle_collisions(self, ball, paddles, alive_players, particle_system, renderer):
        """Check and handle ball-paddle collisions"""
        # Check for ghost ball effect
        has_ghost, ghost_player_id = False, -1
        if self.powerup_system:
            has_ghost, ghost_player_id = self.powerup_system.has_ghost_ball()
        
        for i, paddle in enumerate(paddles):
            if alive_players[i] and ball.rect.colliderect(paddle.rect):
                # Ghost ball passes through enemy paddles
                if has_ghost and i != ghost_player_id:
                    # Ball passes through - add ghost effect particles
                    particle_system.add_particle(ball.x, ball.y, 0, 0, (0, 255, 255, 100), 30)
                    continue
                    
                ball.bounce_off_paddle(paddle)
                # Add particle effect for paddle hit
                particle_system.add_ball_impact_burst(ball.x, ball.y, paddle.color)
                # Add screen shake for paddle hit
                renderer.add_screen_shake(3, 8)
                return True  # Collision occurred
        return False  # No collision
        
    def check_ball_boundary_collisions(self, ball, alive_players, particle_system, renderer, force_bounce=False):
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
            if force_bounce or not alive_players[0]:  # Force bounce for decoy balls or dead player
                ball.bounce_off_wall("left")
                particle_system.add_wall_impact_sparks(ball.x, ball.y)
                renderer.add_screen_shake(1, 4)
                collision_info['bounced'] = True
            elif alive_players[0]:  # Live player
                # Check for shield
                if self.powerup_system and self.powerup_system.has_shield(0):
                    # Use shield instead of losing life
                    self.powerup_system.use_shield(0)
                    ball.bounce_off_wall("left")
                    particle_system.add_wall_impact_sparks(ball.x, ball.y)
                    particle_system.add_shield_break_effect(ball.x, ball.y)
                    renderer.add_screen_shake(5, 10)
                    collision_info['bounced'] = True
                else:
                    # No shield - loses life (only if ball causes life loss)
                    if ball.causes_life_loss():
                        collision_info['life_lost'] = True
                    else:
                        # Decoy ball - just bounce
                        ball.bounce_off_wall("left")
                        particle_system.add_wall_impact_sparks(ball.x, ball.y)
                        renderer.add_screen_shake(1, 4)
                        collision_info['bounced'] = True

        # Check right boundary
        elif ball.x >= SCREEN_WIDTH - BOUNDARY_THICKNESS:
            collision_info['collision_occurred'] = True
            collision_info['player_hit'] = 1
            if force_bounce or not alive_players[1]:  # Force bounce for decoy balls or dead player
                ball.bounce_off_wall("right")
                particle_system.add_wall_impact_sparks(ball.x, ball.y)
                renderer.add_screen_shake(1, 4)
                collision_info['bounced'] = True
            elif alive_players[1]:  # Live player
                # Check for shield
                if self.powerup_system and self.powerup_system.has_shield(1):
                    # Use shield instead of losing life
                    self.powerup_system.use_shield(1)
                    ball.bounce_off_wall("right")
                    particle_system.add_wall_impact_sparks(ball.x, ball.y)
                    particle_system.add_shield_break_effect(ball.x, ball.y)
                    renderer.add_screen_shake(5, 10)
                    collision_info['bounced'] = True
                else:
                    # No shield - loses life (only if ball causes life loss)
                    if ball.causes_life_loss():
                        collision_info['life_lost'] = True
                    else:
                        # Decoy ball - just bounce
                        ball.bounce_off_wall("right")
                        particle_system.add_wall_impact_sparks(ball.x, ball.y)
                        renderer.add_screen_shake(1, 4)
                        collision_info['bounced'] = True

        # Check top boundary
        elif ball.y <= BOUNDARY_THICKNESS:
            collision_info['collision_occurred'] = True
            collision_info['player_hit'] = 2
            if force_bounce or not alive_players[2]:  # Force bounce for decoy balls or dead player
                ball.bounce_off_wall("top")
                particle_system.add_wall_impact_sparks(ball.x, ball.y)
                renderer.add_screen_shake(1, 4)
                collision_info['bounced'] = True
            elif alive_players[2]:  # Live player
                # Check for shield
                if self.powerup_system and self.powerup_system.has_shield(2):
                    # Use shield instead of losing life
                    self.powerup_system.use_shield(2)
                    ball.bounce_off_wall("top")
                    particle_system.add_wall_impact_sparks(ball.x, ball.y)
                    particle_system.add_shield_break_effect(ball.x, ball.y)
                    renderer.add_screen_shake(5, 10)
                    collision_info['bounced'] = True
                else:
                    # No shield - loses life (only if ball causes life loss)
                    if ball.causes_life_loss():
                        collision_info['life_lost'] = True
                    else:
                        # Decoy ball - just bounce
                        ball.bounce_off_wall("top")
                        particle_system.add_wall_impact_sparks(ball.x, ball.y)
                        renderer.add_screen_shake(1, 4)
                        collision_info['bounced'] = True

        # Check bottom boundary
        elif ball.y >= SCREEN_HEIGHT - BOUNDARY_THICKNESS:
            collision_info['collision_occurred'] = True
            collision_info['player_hit'] = 3
            if force_bounce or not alive_players[3]:  # Force bounce for decoy balls or dead player
                ball.bounce_off_wall("bottom")
                particle_system.add_wall_impact_sparks(ball.x, ball.y)
                renderer.add_screen_shake(1, 4)
                collision_info['bounced'] = True
            elif alive_players[3]:  # Live player
                # Check for shield
                if self.powerup_system and self.powerup_system.has_shield(3):
                    # Use shield instead of losing life
                    self.powerup_system.use_shield(3)
                    ball.bounce_off_wall("bottom")
                    particle_system.add_wall_impact_sparks(ball.x, ball.y)
                    particle_system.add_shield_break_effect(ball.x, ball.y)
                    renderer.add_screen_shake(5, 10)
                    collision_info['bounced'] = True
                else:
                    # No shield - loses life (only if ball causes life loss)
                    if ball.causes_life_loss():
                        collision_info['life_lost'] = True
                    else:
                        # Decoy ball - just bounce
                        ball.bounce_off_wall("bottom")
                        particle_system.add_wall_impact_sparks(ball.x, ball.y)
                        renderer.add_screen_shake(1, 4)
                        collision_info['bounced'] = True
                
        return collision_info