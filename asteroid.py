from constants import *
from circleshape import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
       super().__init__(x, y, radius, self.containers)

    def update(self, dt):
        self.position += self.velocity * dt
        self.keep_on_screen(SCREEN_WIDTH, SCREEN_HEIGHT) # Screen wrap

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



