import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, animation_speed):
        super().__init__()
        self.center = center
        self.animation_frames = []
        try:
            for i in range(1, 9): # Assuming 8 frames: explosion_01.png to explosion_08.png
                filename = f"explosion_0{i}.png"
                image = pygame.image.load(filename)
                self.animation_frames.append(image)
        except pygame.error as e:
            print(f"Error loading explosion animation frames: {e}")
            # If any frame is missing, we can't really have an animation.
            # Depending on desired behavior, could have a fallback single image or just an empty list.
            # For now, if frames are missing, animation_frames will be empty or partially filled,
            # which will lead to issues later if not handled.
            # A robust solution might involve a placeholder image or specific error handling in update.
            # However, the prompt implies printing an error is sufficient for missing images.
            pass # Continue, animation_frames might be incomplete

        if not self.animation_frames:
            # If no frames were loaded, we cannot proceed to set up the sprite image/rect
            # This will likely cause a crash if an Explosion instance is created without frames.
            # A better approach would be to self.kill() or raise an error here,
            # or ensure a placeholder image is used.
            # For now, adhering to the prompt's focus on loading and basic error print.
            print("Explosion animation frames failed to load. Explosion will not be visible.")
            return


        self.current_frame = 0
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect(center=self.center)

        self.animation_speed = animation_speed  # frames per second
        self.frame_timer = 0

    def update(self, dt):
        if not self.animation_frames: # If no frames, do nothing (or kill)
            self.kill() # Kill if not properly initialized
            return

        self.frame_timer += dt

        # Time to show one frame is 1.0 / frames_per_second
        if self.frame_timer >= (1.0 / self.animation_speed):
            self.frame_timer = 0 # Reset timer
            self.current_frame += 1
            if self.current_frame >= len(self.animation_frames):
                self.kill() # Animation finished
            else:
                self.image = self.animation_frames[self.current_frame]
                # Update rect as image size might change between frames, keep center consistent
                self.rect = self.image.get_rect(center=self.rect.center)
