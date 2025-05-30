import pygame # Import pygame
from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y):
       super().__init__(x,y, SHOT_RADIUS)
       try:
           self.sprite = pygame.image.load("shot.png")
           # Optionally, scale the sprite if its default size isn't SHOT_RADIUS
           # For now, we assume shot.png is already appropriately sized or doesn't need scaling.
       except pygame.error as e:
           print(f"Error loading shot.png: {e}")
           self.sprite = None # Set sprite to None if loading fails

    def draw(self, screen, color = "white", line_width = 2 ):
        if self.sprite:
            # Adjust position to draw from the center of the sprite
            rect = self.sprite.get_rect(center=self.position)
            screen.blit(self.sprite, rect.topleft)
        else:
            # Fallback to drawing a circle if sprite loading failed
            pygame.draw.circle(screen, color, self.position, self.radius, line_width)

    def update(self, dt):
        self.position += self.velocity * dt