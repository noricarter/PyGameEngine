class Platform:
    def __init__(self, world_x, world_y, width, height, color=(200, 200, 200)):
        self.world_x = world_x
        self.world_y = world_y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen, camera):
        #Draw platform to the screen using the camera offset.
        screen_x, screen_y = camera.world_to_screen(self.world_x, self.world_y)
        import pygame
        pygame.draw.rect(screen, self.color, (screen_x, screen_y, self.width, self.height))
