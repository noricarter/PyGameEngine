import math
import random
from typing import List
import pygame

from entities import Obstacle
from settings import (
    WIDTH, HEIGHT, GROUND_Y, GROUND, BG,
    OB_MIN_W, OB_MAX_W, OB_MIN_H, OB_MAX_H,
    OB_GAP_MIN, SPAWN_COOLDOWN_MIN, SPAWN_COOLDOWN_MAX,
    BASE_SPEED, OB_COLOR
)

class World:
    def __init__(self):
        self.obstacles: List[Obstacle] = []
        self.distance = 0.0
        self.stripe_offset = 0.0
        self.time_since_spawn = 0.0
        # Pre-build ground stripes
        self.ground_stripes = [pygame.Rect(i * 40, GROUND_Y + 30, 30, 5)
                               for i in range((WIDTH // 40) + 4)]

    def reset(self):
        self.obstacles.clear()
        self.distance = 0.0
        self.time_since_spawn = 0.0

    # --- difficulty ---
    def current_speed(self) -> float:
        # Speed increases with distance; smooth non-linear growth
        return BASE_SPEED + 1.5 * math.sqrt(max(self.distance, 0) / 300.0)

    def spawn_cooldown(self, speed: float) -> float:
        t = max(0.0, min(1.0, (speed - BASE_SPEED) / 8.0))
        return SPAWN_COOLDOWN_MAX * (1 - t) + SPAWN_COOLDOWN_MIN * t

    def maybe_spawn(self, speed: float):
        w = random.randint(OB_MIN_W, OB_MAX_W)
        h = random.randint(OB_MIN_H, OB_MAX_H)
        if self.obstacles:
            rightmost = max(ob.x + ob.w for ob in self.obstacles)
        else:
            rightmost = 0
        desired_gap = max(140, OB_GAP_MIN - (speed * 6))
        if rightmost < WIDTH - desired_gap:
            self.obstacles.append(Obstacle(WIDTH + random.randint(0, 60), w, h))

    # --- update loops ---
    def update_menu(self, dt: float):
        """True idle menu: no spawns, no obstacle movement, no distance gain."""
        self.obstacles.clear()
        self.distance = 0.0
        self.time_since_spawn = 0.0
        # Mild background stripe motion so the menu isn't static
        self.stripe_offset = (self.stripe_offset + BASE_SPEED * 0.6) % 40

    def update_play(self, dt: float):
        speed = self.current_speed()
        self.distance += speed * dt * 60
        # Move obstacles
        for ob in list(self.obstacles):
            ob.update(speed)
        self.obstacles = [o for o in self.obstacles if o.x + o.w > -10]
        # Spawn
        self.time_since_spawn += dt
        if self.time_since_spawn >= self.spawn_cooldown(speed):
            self.maybe_spawn(speed)
            self.time_since_spawn = 0.0
        # Ground stripes
        self.stripe_offset = (self.stripe_offset + speed) % 40

    # --- drawing ---
    def draw_background(self, screen: pygame.Surface):
        screen.fill(BG)
        pygame.draw.rect(screen, GROUND, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        for r in self.ground_stripes:
            rr = r.copy()
            rr.x = (r.x - int(self.stripe_offset)) % (WIDTH + 160)
            pygame.draw.rect(screen, (55, 55, 75), rr)

    def draw_obstacles(self, screen: pygame.Surface):
        for ob in self.obstacles:
            ob.draw(screen, OB_COLOR)
