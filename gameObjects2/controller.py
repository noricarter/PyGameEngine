import pygame

class Controller:
    def __init__(self, up=pygame.K_UP, down=pygame.K_DOWN, left=pygame.K_LEFT, right=pygame.K_RIGHT):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.speed = 0  # default, will be set by the player

    def set_speed(self, speed):
        self.speed = speed

    def get_movement(self, dt):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[self.up]:
            dy -= self.speed * dt
        if keys[self.down]:
            dy += self.speed * dt
        if keys[self.left]:
            dx -= self.speed * dt
        if keys[self.right]:
            dx += self.speed * dt

        return dx, dy