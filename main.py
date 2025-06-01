import pygame
import constants
from player import *
from asteroidfield import *
from shot import Shot
import sys

def main():
    pygame.init()
    pygame.font.init() # Initialize font module
    print("Starting Asteroids!")
    print(f"Screen width: {constants.SCREEN_WIDTH}")
    print(f"Screen height: {constants.SCREEN_HEIGHT}")

    dt = 0
    gameclock = pygame.time.Clock()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group() 
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots) 

    player = Player(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
    asteroidfield1 = AsteroidField()
   # player.Containers = (updatable, drawable)

    font = pygame.font.Font(None, 36) # Create font object

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
                    obj.split()
                    shot.kill()
                    constants.SUCCESSFUL_HITS += 1

        for obj in drawable:
            obj.draw(screen)

        # Display score
        text_surface = font.render(f"Hits: {constants.SUCCESSFUL_HITS}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        dt = gameclock.tick(60) /1000


if __name__ == "__main__":
    main()
