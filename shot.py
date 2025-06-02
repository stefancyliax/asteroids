from constants import *
from circleshape import *

class Shot(CircleShape):
    def __init__(self, x, y):
       super().__init__(x, y, SHOT_RADIUS, self.containers)

    def update(self, dt):
        self.position += self.velocity * dt