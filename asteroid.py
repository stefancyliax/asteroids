import constants
from circleshape import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
       super().__init__(x,y, radius)

    def draw(self, screen, color = "white", line_width = 2 ):
        pygame.draw.circle(screen, color, self.position, self.radius, line_width)
        return

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius < constants.ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20,50)
            part_radius = self.radius - constants.ASTEROID_MIN_RADIUS
            
            asteroid_part_1 = Asteroid(self.position.x, self.position.y, part_radius)
            asteroid_part_1.velocity = self.velocity.rotate(random_angle) * 1.2
            asteroid_part_2 = Asteroid(self.position.x, self.position.y, part_radius)
            asteroid_part_2.velocity = self.velocity.rotate(-random_angle) * 1.2



