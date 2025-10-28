from dataclasses import dataclass
import pygame
from settings import PLAYER_W, PLAYER_H, GROUND_Y, PLAYER_COLOR, GRAVITY, JUMP_VELOCITY

@dataclass
class Player:
    x: float
    y: float
    vy: float = 0
    on_ground: bool = True

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), PLAYER_W, PLAYER_H)

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_VELOCITY
            self.on_ground = False

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        if self.y + PLAYER_H >= GROUND_Y:
            self.y = GROUND_Y - PLAYER_H
            self.vy = 0
            self.on_ground = True

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, PLAYER_COLOR, self.rect(), border_radius=10)

@dataclass
class Obstacle:
    x: float
    w: int
    h: int

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), GROUND_Y - self.h, self.w, self.h)

    def update(self, dx: float):
        self.x -= dx

    def draw(self, surf: pygame.Surface, color):
        pygame.draw.rect(surf, color, self.rect(), border_radius=6)
