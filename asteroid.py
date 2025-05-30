import pygame # Import pygame
from constants import *
from circleshape import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
       super().__init__(x,y, radius)
       try:
           self.sprite = pygame.image.load("asteroid.png")
           # Scale the sprite to the asteroid's radius
           # We'll scale it to fit within a square of side length 2*radius
           self.sprite = pygame.transform.scale(self.sprite, (int(2 * self.radius), int(2 * self.radius)))
       except pygame.error as e:
           print(f"Error loading asteroid.png: {e}")
           self.sprite = None # Set sprite to None if loading fails

    def draw(self, screen, color = "white", line_width = 2 ):
        if self.sprite:
            # Adjust position to draw from the center of the sprite
            rect = self.sprite.get_rect(center=self.position)
            screen.blit(self.sprite, rect.topleft)
        else:
            # Fallback to drawing a circle if sprite loading failed
            pygame.draw.circle(screen, color, self.position, self.radius, line_width)
        return

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius < ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20,50)
            part_radius = self.radius - ASTEROID_MIN_RADIUS
            
            asteroid_part_1 = Asteroid(self.position.x, self.position.y, part_radius)
            asteroid_part_1.velocity = self.velocity.rotate(random_angle) * 1.2
            asteroid_part_2 = Asteroid(self.position.x, self.position.y, part_radius)
            asteroid_part_2.velocity = self.velocity.rotate(-random_angle) * 1.2



