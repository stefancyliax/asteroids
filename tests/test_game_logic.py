import unittest
import sys
import os

# Add project root to sys.path to allow importing game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize Pygame minimally if required by the modules,
# especially for pygame.Vector2. This might need to be conditional
# or handled by mocking if full pygame init is problematic in tests.
pygame_module_mocked = False
try:
    import pygame
    pygame.init() # Initialize relevant pygame modules, not necessarily full display
except (ImportError, NameError) as e: # Catch if pygame itself is not found
    print(f"Warning: Pygame module not found or error during import: {e}. Using mock objects.")
    pygame_module_mocked = True
except pygame.error as e: # Catch specific pygame errors if module was found but init failed
    print(f"Warning: Pygame could not be initialized in tests: {e}. Using mock objects.")
    pygame_module_mocked = True

if pygame_module_mocked:
    # Define a dummy Vector2 if pygame fails to load or initialize
    class DummyVector2:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __add__(self, other):
            return DummyVector2(self.x + other.x, self.y + other.y)
        def __sub__(self, other):
            return DummyVector2(self.x - other.x, self.y - other.y)
        def __mul__(self, scalar):
            return DummyVector2(self.x * scalar, self.y * scalar)
        def rotate(self, angle_degrees):
            # Simplified rotation, not accurate, for placeholder if needed
            return self
        def distance_to(self, other):
            return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    # Define a dummy sprite module with Group and Sprite
    class DummySprite(object): # Base class for sprites
        def __init__(self, *groups):
            self._groups = set()
            if groups:
                for group in groups:
                    group.add(self)

        def add(self, *groups):
            for group in groups:
                group.add(self)
                self._groups.add(id(group))

        def kill(self):
            for group_id in list(self._groups): # Iterate over a copy for modification
                # This requires groups to be findable or stored in a way kill can access them
                # For simplicity, assume groups have a 'remove' method and are tracked.
                # This mock is getting complex; real mocking libraries (unittest.mock) are better.
                # However, if Asteroid.containers holds actual DummyGroup instances, it works.
                pass # In a real scenario, this would remove self from groups.
            self._groups.clear()

        def groups(self):
            # This would need a way to get back the actual group objects
            return []


    class DummyGroup(set): # Inherit from set for basic group operations
        def __init__(self, *sprites):
            super().__init__()
            if sprites:
                for sprite in sprites:
                    self.add(sprite)

        def add(self, *sprites):
            for sprite in sprites:
                super().add(sprite)
                if hasattr(sprite, '_groups'): # If it's a DummySprite
                     sprite._groups.add(id(self))


        def remove(self, *sprites):
            for sprite in sprites:
                if sprite in self:
                    super().remove(sprite)
                if hasattr(sprite, '_groups') and id(self) in sprite._groups:
                     sprite._groups.remove(id(self))

        def empty(self):
            # For DummySprite, need to tell them they are removed from this group
            all_sprites = list(self)
            for sprite in all_sprites:
                self.remove(sprite)
            super().empty()


    pygame = type('pygame', (object,), {
        'Vector2': DummyVector2,
        'sprite': type('sprite', (object,), {
            'Group': DummyGroup,
            'Sprite': DummySprite
        }),
        'error': type('error', (Exception,), {}) # Define pygame.error for the except block
    })


from circleshape import CircleShape
from asteroid import Asteroid
from constants import ASTEROID_MIN_RADIUS, ASTEROID_KINDS # For asteroid splitting

class TestCircleShape(unittest.TestCase):
    def test_collision_detection(self):
        # Test collision
        shape1 = CircleShape(0, 0, 10)
        shape2 = CircleShape(15, 0, 10) # (0,0,r=10) and (15,0,r=10) should collide (dist=15, sum_radii=20)
        self.assertTrue(shape1.collision(shape2), "Shapes should collide")

        # Test no collision
        shape3 = CircleShape(0, 0, 10)
        shape4 = CircleShape(25, 0, 10) # (0,0,r=10) and (25,0,r=10) should not collide (dist=25, sum_radii=20)
        self.assertFalse(shape3.collision(shape4), "Shapes should not collide")

        # Test edge case: just touching
        shape5 = CircleShape(0, 0, 10)
        shape6 = CircleShape(20, 0, 10) # (0,0,r=10) and (20,0,r=10) should collide (dist=20, sum_radii=20)
        self.assertTrue(shape5.collision(shape6), "Shapes should collide when touching")

    def test_collision_with_zero_radius(self):
        shape1 = CircleShape(0, 0, 10)
        shape2 = CircleShape(5, 0, 0)
        self.assertTrue(shape1.collision(shape2), "Collision with zero radius shape within larger shape")

        shape3 = CircleShape(0, 0, 0)
        shape4 = CircleShape(0, 0, 0)
        self.assertTrue(shape3.collision(shape4), "Collision of two zero radius shapes at same point")

class TestAsteroid(unittest.TestCase):
    def setUp(self):
        # Asteroids need to be added to sprite groups for kill() to work.
        # We can mock this or ensure containers are set if necessary.
        # For now, let's assume kill() works without actual groups for logic test.
        # If Asteroid.containers is not set, kill() might fail.
        # Minimal setup for Asteroid.containers. It should be a tuple of groups.
        if not hasattr(Asteroid, 'containers') or Asteroid.containers is None:
            # Ensure pygame.sprite.Group is the one from our mock if pygame is mocked
            GroupClass = pygame.sprite.Group if hasattr(pygame, 'sprite') and hasattr(pygame.sprite, 'Group') else set
            Asteroid.containers = (GroupClass(), GroupClass(), GroupClass())

    def test_asteroid_split(self):
        # Create an asteroid large enough to split
        initial_radius = ASTEROID_MIN_RADIUS * 2
        asteroid = Asteroid(100, 100, initial_radius)
        asteroid.velocity = pygame.Vector2(10, 0) # Give it some velocity

        original_kill = asteroid.kill
        killed_self = False
        def mock_kill():
            nonlocal killed_self
            killed_self = True
            # original_kill() # Don't actually call original if it needs groups
        asteroid.kill = mock_kill

        asteroid.split()

        self.assertTrue(killed_self, "Original asteroid should be killed after splitting")
        # Restore original kill method to avoid affecting other tests if any
        asteroid.kill = original_kill


    def test_asteroid_no_split_if_too_small(self):
        # Create an asteroid too small to split
        initial_radius = ASTEROID_MIN_RADIUS / 2
        asteroid = Asteroid(100, 100, initial_radius)
        asteroid.velocity = pygame.Vector2(10, 0)

        original_kill = asteroid.kill
        killed_self = False
        def mock_kill():
            nonlocal killed_self
            killed_self = True
        asteroid.kill = mock_kill

        asteroid.split()

        self.assertTrue(killed_self, "Small asteroid should still be killed (disappear)")
        asteroid.kill = original_kill


class TestAsteroidSplitProper(unittest.TestCase):
    def setUp(self):
        self.updatable_group = pygame.sprite.Group()
        self.drawable_group = pygame.sprite.Group()
        self.asteroids_group = pygame.sprite.Group()

        # Set the class attribute 'containers' for Asteroid instances
        # Ensure these groups are instances of our DummyGroup if pygame is mocked
        GroupClass = pygame.sprite.Group if hasattr(pygame, 'sprite') and hasattr(pygame.sprite, 'Group') else set
        self.updatable_group = GroupClass()
        self.drawable_group = GroupClass()
        self.asteroids_group = GroupClass()
        Asteroid.containers = (self.updatable_group, self.drawable_group, self.asteroids_group)

        # Clear group at setup to ensure clean state for each test
        if hasattr(self.asteroids_group, 'empty'):
            self.asteroids_group.empty()
        else: # for basic set
            self.asteroids_group.clear()


    def test_asteroid_split_creates_new_asteroids(self):
        initial_radius = ASTEROID_MIN_RADIUS * 2 # Large enough to split
        # Ensure the original asteroid is part of a group that its kill method can affect
        # This also means it will be removed from self.asteroids_group upon kill()
        asteroid = Asteroid(50, 50, initial_radius)
        asteroid.velocity = pygame.Vector2(5, 5)

        # Add the original asteroid to the group to test it's removed.
        # self.asteroids_group.add(asteroid) # Asteroid adds itself on init due to containers

        # The group should contain 1 (the original asteroid) if it adds itself on init
        # self.assertEqual(len(self.asteroids_group), 1, "Group should initially contain the main asteroid")
        # No, Asteroid() call above already adds it to the group via containers.
        # So, to check only *new* asteroids, we must count before and after, or clear then count.
        # setUp already clears the group. So Asteroid() will add itself.

        count_before_split = len(self.asteroids_group) # Should be 1 if asteroid adds itself

        asteroid.split() # This should kill the original and add two new ones

        # The original asteroid (count_before_split=1) is killed, 2 new are added.
        # So, total in group should be 2.
        self.assertEqual(len(self.asteroids_group), 2, "Splitting should result in two new asteroids in the group")

        new_radius_expected = initial_radius - ASTEROID_MIN_RADIUS
        for new_asteroid in self.asteroids_group:
            self.assertEqual(new_asteroid.radius, new_radius_expected, "New asteroid has incorrect radius")
            self.assertTrue(isinstance(new_asteroid, Asteroid), "New object should be an Asteroid")


    def test_asteroid_no_split_if_too_small_and_no_new_asteroids(self):
        initial_radius = ASTEROID_MIN_RADIUS / 2 # Too small to split
        asteroid = Asteroid(50, 50, initial_radius)
        asteroid.velocity = pygame.Vector2(5, 5)

        # Asteroid adds itself to self.asteroids_group on creation.
        # So, the group has 1 asteroid. After split, it should be killed and none added.

        asteroid.split()

        self.assertEqual(len(self.asteroids_group), 0, "Splitting a small asteroid should remove it and not create new ones")


if __name__ == '__main__':
    unittest.main()
