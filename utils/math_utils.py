import pygame
import math

class Vector2:
    """Simple 2D vector class for ball movement"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def normalize(self):
        """Normalize the vector to unit length"""
        length = math.sqrt(self.x**2 + self.y**2)
        if length > 0:
            return Vector2(self.x / length, self.y / length)
        return Vector2(0, 0)

    def magnitude(self):
        """Get the magnitude of the vector"""
        return math.sqrt(self.x**2 + self.y**2)

def clamp(value, min_val, max_val):
    """Clamp a value between min and max"""
    return max(min_val, min(value, max_val))

def distance(pos1, pos2):
    """Calculate distance between two points"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def reflect_vector(vector, normal):
    """Reflect a vector off a surface with given normal"""
    # v' = v - 2(v·n)n
    dot_product = vector.x * normal.x + vector.y * normal.y
    return Vector2(
        vector.x - 2 * dot_product * normal.x,
        vector.y - 2 * dot_product * normal.y
    )