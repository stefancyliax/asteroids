import pygame # Import pygame
from constants import *
from circleshape import *
from main import *

class Player(CircleShape):
    def __init__(self, x, y):
       super().__init__(x,y,PLAYER_RADIUS)
       self.rotation = 0
       self.shot_timer = 0
       try:
           self.sprite = pygame.image.load("player_ship.png")
       except pygame.error as e:
           print(f"Error loading player_ship.png: {e}")
           self.sprite = None # Set sprite to None if loading fails

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen, color = "white", line_width = 2 ):
        if self.sprite:
            # Pygame's rotate function rotates counter-clockwise, so we negate the angle
            # to match the existing rotation direction if necessary.
            # However, the existing triangle method uses self.rotation directly,
            # so we'll assume self.rotation is already in the correct orientation.
            rotated_sprite = pygame.transform.rotate(self.sprite, -self.rotation)
            # Adjust position to draw from the center of the sprite
            rect = rotated_sprite.get_rect(center=self.position)
            screen.blit(rotated_sprite, rect.topleft)
        else:
            # Fallback to drawing a triangle if sprite loading failed
            pygame.draw.polygon(screen, color, self.triangle(), line_width)
        return

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.shot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE] and not self.shot_timer > 0:
            self.shoot()
                
         

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
        self.shot_timer = 0.3