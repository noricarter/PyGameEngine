import pygame

class Player:
    def __init__(self, x, y, controller, color=(50, 0, 50)):
        self.x = x
        self.y = y
        self.controller = controller

        # Future physics fields (kept here for uniformity later)
        self.vx = 0.0
        self.vy = 0.0
        self.mass = 1.0
        self.radius = 10

        # Appearance data (World will use this to draw)
        self.appearance = {"type": "circle", "color": (255, 255, 0)}

        # Movement tuning (temporary, no physics yet)
        self.move_speed = 3.0

    def update(self, dt):
        # Simple direct movement for now (no physics force integration yet)
        dx = (self.controller.right - self.controller.left) * self.move_speed * dt
        dy = (self.controller.down - self.controller.up) * self.move_speed * dt
        self.x += dx
        self.y += dy