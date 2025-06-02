from constants import *
from circleshape import *
# Removed: from main import *

class Player(CircleShape):
    def __init__(self, x, y, shoot_sound_obj): # Added shoot_sound_obj
       super().__init__(x, y, PLAYER_RADIUS, self.containers)
       self.rotation = 0
       self.shot_timer = 0
       self.shoot_sound = shoot_sound_obj # Store shoot_sound_obj

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen, color = "white", line_width = 2 ):
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

        self.keep_on_screen(SCREEN_WIDTH, SCREEN_HEIGHT) # Screen wrap
         

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN
        self.shoot_sound.play() # Play the sound