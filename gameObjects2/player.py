import pygame

class Player:
    def __init__(self, x, y, controller, color=(50, 0, 50)):
        self.x = x
        self.y = y
        self.controller = controller
        self.color = color
        self.speed = 1
        self.controller.set_speed(self.speed)

    def update(self, dt):
        if self.controller:
            dx, dy = self.controller.get_movement(dt)
            self.x += dx
            self.y += dy

    def draw(self, screen, screenW, screenH):
        cx = screenW / 2
        cy = screenH / 2

        pygame.draw.polygon(
            screen,
            self.color,
            [
                (cx, cy - 10),
                (cx - 10, cy + 10),
                (cx + 10, cy + 10)
            ]
        )
