import pygame
import random
import math
from utils.constants import *

class Particle:
    def __init__(self, x, y, velocity_x, velocity_y, color, size, lifetime):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = 0.1

    def update(self):
        """Update particle position and lifetime"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity  # Add gravity effect
        self.velocity_x *= 0.98  # Air resistance
        self.velocity_y *= 0.98
        self.lifetime -= 1
        return self.lifetime > 0

    def get_alpha(self):
        """Get current alpha based on remaining lifetime"""
        return int(255 * (self.lifetime / self.max_lifetime))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_ball_impact_burst(self, x, y, paddle_color):
        """Create particle burst when ball hits paddle"""
        particle_count = random.randint(8, 12)
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            # Mix paddle color with white for sparks
            spark_color = tuple(min(255, int(c * 0.8 + 255 * 0.2)) for c in paddle_color)
            
            size = random.uniform(2, 4)
            lifetime = random.randint(15, 30)
            
            self.particles.append(Particle(x, y, velocity_x, velocity_y, spark_color, size, lifetime))

    def add_wall_impact_sparks(self, x, y):
        """Create small sparks when ball hits wall"""
        particle_count = random.randint(4, 6)
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            spark_color = NEON_BLUE
            size = random.uniform(1, 2)
            lifetime = random.randint(10, 20)
            
            self.particles.append(Particle(x, y, velocity_x, velocity_y, spark_color, size, lifetime))
    
    def add_victory_celebration(self, x, y, winner_color):
        """Create victory celebration effect for the last surviving player"""
        particle_count = random.randint(50, 70)
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(4, 10)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed - 4  # Strong upward bias
            
            # Bright, sparkling colors
            sparkle_factor = random.uniform(0.7, 1.0)
            victory_color = tuple(min(255, int(c * sparkle_factor + 255 * (1 - sparkle_factor))) for c in winner_color)
            
            size = random.uniform(3, 7)
            lifetime = random.randint(60, 100)  # Long lasting celebration
            
            self.particles.append(Particle(x, y, velocity_x, velocity_y, victory_color, size, lifetime))

    def add_score_celebration(self, x, y, player_color):
        """Create celebration particles when player scores"""
        particle_count = random.randint(15, 20)
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed - 2  # Upward bias
            
            size = random.uniform(3, 6)
            lifetime = random.randint(30, 50)
            
            self.particles.append(Particle(x, y, velocity_x, velocity_y, player_color, size, lifetime))
    
    def add_elimination_effect(self, x, y, player_color):
        """Create dramatic elimination effect when player dies"""
        # Large explosion of particles
        particle_count = random.randint(30, 40)
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(5, 12)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            # Mix player color with red for dramatic effect
            red_intensity = random.uniform(0.5, 1.0)
            elimination_color = (
                int(player_color[0] * (1 - red_intensity) + 255 * red_intensity),
                int(player_color[1] * (1 - red_intensity)),
                int(player_color[2] * (1 - red_intensity))
            )
            
            size = random.uniform(4, 8)  # Larger particles
            lifetime = random.randint(40, 70)  # Longer lasting
            
            self.particles.append(Particle(x, y, velocity_x, velocity_y, elimination_color, size, lifetime))
        
        # Add some pure red "death" particles
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed - 3  # Slight upward bias
            
            size = random.uniform(2, 4)
            lifetime = random.randint(50, 80)
            
            self.particles.append(Particle(x, y, velocity_x, velocity_y, (255, 0, 0), size, lifetime))

    def update(self):
        """Update all particles and remove dead ones"""
        self.particles = [p for p in self.particles if p.update()]

    def render(self, screen):
        """Render all particles with alpha blending"""
        for particle in self.particles:
            alpha = particle.get_alpha()
            if alpha > 0:
                # Create surface with alpha
                particle_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
                color_with_alpha = (*particle.color, alpha)
                pygame.draw.circle(particle_surface, color_with_alpha, 
                                 (particle.size, particle.size), particle.size)
                
                # Add glow effect
                glow_size = particle.size * 1.5
                glow_alpha = alpha // 3
                if glow_alpha > 0:
                    glow_color = (*particle.color, glow_alpha)
                    pygame.draw.circle(particle_surface, glow_color,
                                     (particle.size, particle.size), glow_size)
                
                screen.blit(particle_surface, (particle.x - particle.size, particle.y - particle.size))

    def clear(self):
        """Remove all particles"""
        self.particles.clear()