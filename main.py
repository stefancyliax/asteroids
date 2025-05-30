import pygame
from constants import *
from player import *
from asteroidfield import *
from shot import Shot
from explosion import Explosion # Import Explosion
import sys

def main():
    pygame.init()
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    dt = 0
    gameclock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group() 
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group() # Create explosions group

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots) 
    Explosion.containers = (updatable, drawable, explosions) # Set Explosion containers

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield1 = AsteroidField()
   # player.Containers = (updatable, drawable)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0,0,0))
        updatable.update(dt)

        for obj in asteroids:
            if player.collision(obj):
                print("Game over!")
                sys.exit()

        for obj in asteroids:
            for shot in shots:
                if shot.collision(obj):
                    Explosion(center=obj.position, animation_speed=10) # Create Explosion instance
                    obj.split()
                    shot.kill()

        for obj in drawable:
            obj.draw(screen)


        pygame.display.flip()
        dt = gameclock.tick(60) /1000


if __name__ == "__main__":
    main()
