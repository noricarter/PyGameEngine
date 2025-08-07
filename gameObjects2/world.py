import pygame

class World:
    def __init__(self, x, y, size, color=(0, 200, 100)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, screen, camera):
        screen_x, screen_y = camera.apply(self.x, self.y)
        pygame.draw.rect(
            screen,
            self.color,
            (screen_x, screen_y, self.size, self.size)
        )
