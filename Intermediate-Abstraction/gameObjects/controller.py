class Controller:
    def __init__(self):
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0

    def update(self, keys):
        self.left  = 1 if keys[pygame.K_LEFT]  or keys[pygame.K_a] else 0
        self.right = 1 if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0
        self.up    = 1 if keys[pygame.K_UP]    or keys[pygame.K_w] else 0
        self.down  = 1 if keys[pygame.K_DOWN]  or keys[pygame.K_s] else 0

import pygame  # at bottom to avoid circular import issues
