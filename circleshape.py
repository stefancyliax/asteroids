import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, *groups):
        super().__init__(*groups)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen, color="white", line_width=2):
        pygame.draw.circle(screen, color, self.position, self.radius, line_width)

    def update(self, dt):
        # sub-classes must override
        pass

    def collision(self, CircleShape):
        #print(self.position.distance_to(CircleShape.position))
        return self.position.distance_to(CircleShape.position) <= (self.radius + CircleShape.radius)

    def keep_on_screen(self, screen_width, screen_height):
        if self.position.x > screen_width + self.radius:
            self.position.x = -self.radius
        elif self.position.x < -self.radius:
            self.position.x = screen_width + self.radius

        if self.position.y > screen_height + self.radius:
            self.position.y = -self.radius
        elif self.position.y < -self.radius:
            self.position.y = screen_height + self.radius