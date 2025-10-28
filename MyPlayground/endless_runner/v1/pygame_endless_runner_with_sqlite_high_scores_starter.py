"""
Endless Runner (Pygame + SQLite)
---------------------------------
A single-file teaching starter that demonstrates:
- Pygame game loop, input, rendering
- Endless runner mechanics with increasing difficulty over time
- Distance-based scoring
- SQLite high scores (save/load top scores)
- Simple name entry on Game Over

Controls
--------
Space / Up Arrow : Jump
R                  : Restart from Game Over
Esc                : Quit
Enter              : Submit name on Game Over

How to run
---------
1) pip install pygame
2) python endless_runner.py  (or whatever filename you save this as)

Packaging (Windows)
-------------------
py -m pip install pyinstaller
py -m PyInstaller --noconsole --onefile --name EndlessRunner main.py

Notes for teaching
------------------
- The DB is stored under %LOCALAPPDATA%/EndlessRunner/scores.db on Windows (and a user-data dir on other OSes).
- Difficulty increases as the distance grows: speed scales up and spawn intervals shrink.
- The code intentionally favors clarity over micro-optimizations—great for students to read and modify.
"""

import math
import os
import random
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import pygame

# ------------------------------
# Utility: per-user data folder
# ------------------------------
APP_NAME = "EndlessRunner"

def user_data_dir() -> Path:
    if sys.platform.startswith("win"):
        base = os.getenv("LOCALAPPDATA") or str(Path.home() / "AppData/Local")
        d = Path(base) / APP_NAME
    elif sys.platform == "darwin":
        d = Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        d = Path.home() / f".{APP_NAME.lower()}"
    d.mkdir(parents=True, exist_ok=True)
    return d

DB_PATH = user_data_dir() / "scores.db"

# ------------------------------
# SQLite helpers
# ------------------------------

def db_connect():
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scores(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                points INTEGER NOT NULL,
                ts DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    return conn

def add_score(player: str, points: int) -> None:
    player = player.strip() or "Player"
    with db_connect() as conn:
        conn.execute("INSERT INTO scores(player, points) VALUES (?, ?)", (player, points))


def best_score() -> int:
    with db_connect() as conn:
        cur = conn.execute("SELECT MAX(points) FROM scores")
        (mx,) = cur.fetchone()
        return mx or 0


def top_scores(limit: int = 5) -> List[Tuple[str, int]]:
    with db_connect() as conn:
        cur = conn.execute(
            "SELECT player, points FROM scores ORDER BY points DESC, ts ASC LIMIT ?",
            (limit,),
        )
        return list(cur.fetchall())


# ------------------------------
# Game Config
# ------------------------------
WIDTH, HEIGHT = 900, 520
GROUND_Y = HEIGHT - 80
FPS = 60

# player
PLAYER_W, PLAYER_H = 50, 60
JUMP_VELOCITY = -15.0
GRAVITY = 0.8

# speed / difficulty
BASE_SPEED = 7.0
SPEED_GROWTH = 0.0025  # growth per unit of distance
SPAWN_COOLDOWN_MIN = 0.65  # seconds at high speed
SPAWN_COOLDOWN_MAX = 1.4   # seconds at low speed

# obstacle
OB_MIN_W, OB_MAX_W = 30, 60
OB_MIN_H, OB_MAX_H = 30, 80
OB_GAP_MIN = 220  # min pixels between obstacles at spawn time (will compress with speed)

# colors
BG = (22, 22, 28)
GROUND = (40, 40, 55)
PLAYER_COLOR = (240, 240, 255)
OB_COLOR = (90, 210, 140)
TEXT = (230, 233, 240)
ACCENT = (255, 209, 102)

# ------------------------------
# Entities
# ------------------------------
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
        # Apply gravity and move
        self.vy += GRAVITY
        self.y += self.vy
        # Ground collision
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

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, OB_COLOR, self.rect(), border_radius=6)


# ------------------------------
# Game State
# ------------------------------
STATE_MENU = "menu"
STATE_PLAY = "play"
STATE_GAME_OVER = "game_over"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Endless Runner • Pygame + SQLite")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 26)
        self.big = pygame.font.SysFont("consolas", 40, bold=True)

        self.reset_run()
        self.state = STATE_MENU
        self.name_input = ""

        # Precompute ground stripe pattern
        self.ground_stripes = [
            pygame.Rect(i * 40, GROUND_Y + 30, 30, 5) for i in range((WIDTH // 40) + 4)
        ]
        self.stripe_offset = 0.0

    def reset_run(self):
        self.player = Player(120, GROUND_Y - PLAYER_H)
        self.obstacles: List[Obstacle] = []
        self.distance = 0.0  # used for scoring (in pixels)
        self.time_since_spawn = 0.0
        self.last_gap_x = WIDTH
        self.speed = BASE_SPEED
        self.game_over_score = 0

    # ------------ difficulty & spawn logic ------------
    def current_speed(self) -> float:
        # Speed increases with distance; smooth non-linear growth.
        # Example: speed = base + k * sqrt(distance / 300)
        return BASE_SPEED + 1.5 * math.sqrt(max(self.distance, 0) / 300.0)

    def spawn_cooldown(self) -> float:
        # As speed rises, spawn slightly more often
        spd = self.speed
        t = max(0.0, min(1.0, (spd - BASE_SPEED) / 8.0))  # normalized 0..1
        return SPAWN_COOLDOWN_MAX * (1 - t) + SPAWN_COOLDOWN_MIN * t

    def maybe_spawn(self):
        # Random obstacle width/height
        w = random.randint(OB_MIN_W, OB_MAX_W)
        h = random.randint(OB_MIN_H, OB_MAX_H)

        # Keep decent spacing by checking last obstacle's x
        if self.obstacles:
            rightmost = max(ob.x + ob.w for ob in self.obstacles)
        else:
            rightmost = 0

        desired_gap = max(140, OB_GAP_MIN - (self.speed * 6))
        if rightmost < WIDTH - desired_gap:
            self.obstacles.append(Obstacle(WIDTH + random.randint(0, 60), w, h))

    # ------------ update & collisions ------------
    def update_play(self, dt: float):
        # Distance & speed
        self.distance += self.speed * dt * 60  # normalize to ~pixels/frame notion
        self.speed = self.current_speed()

        # Player update
        self.player.update()

        # Move obstacles
        for ob in list(self.obstacles):
            ob.update(self.speed)
        # Remove off-screen
        self.obstacles = [o for o in self.obstacles if o.x + o.w > -10]

        # Spawn logic
        self.time_since_spawn += dt
        if self.time_since_spawn >= self.spawn_cooldown():
            self.maybe_spawn()
            self.time_since_spawn = 0.0

        # Collision
        pr = self.player.rect()
        for ob in self.obstacles:
            if pr.colliderect(ob.rect()):
                self.end_run()
                break

        # Move ground stripes for parallax effect
        self.stripe_offset = (self.stripe_offset + self.speed) % 40

    def update_menu(self, dt: float):
        """Idle animation only: no distance, no spawns, no collisions."""
        # Keep player grounded and stationary
        self.player.y = GROUND_Y - PLAYER_H
        self.player.vy = 0
        self.player.on_ground = True
        # Clear any obstacles lingering from previous runs
        self.obstacles = []
        # Gentle ground stripe scroll for life
        self.stripe_offset = (self.stripe_offset + BASE_SPEED * 0.6) % 40


    def end_run(self):
        self.state = STATE_GAME_OVER
        self.game_over_score = int(self.distance // 5)  # scale down for nicer numbers
        self.name_input = ""

    # ---------------- drawing ----------------
    def draw_world(self):
        self.screen.fill(BG)
        # Ground
        pygame.draw.rect(self.screen, GROUND, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        # Stripes
        for i, r in enumerate(self.ground_stripes):
            rr = r.copy()
            rr.x = (r.x - int(self.stripe_offset)) % (WIDTH + 160)
            pygame.draw.rect(self.screen, (55, 55, 75), rr)

        # Obstacles & Player
        for ob in self.obstacles:
            ob.draw(self.screen)
        self.player.draw(self.screen)

    def draw_hud(self):
        score = int(self.distance // 5)
        s = self.font.render(f"Score: {score}", True, TEXT)
        self.screen.blit(s, (20, 16))
        b = self.font.render(f"Best: {best_score()}", True, ACCENT)
        self.screen.blit(b, (20, 46))

    def draw_menu(self):
        self.draw_world()
        title = self.big.render("ENDLESS RUNNER", True, ACCENT)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 90))

        tip = self.font.render("Press SPACE to Start • Esc to Quit", True, TEXT)
        self.screen.blit(tip, (WIDTH//2 - tip.get_width()//2, 150))

        # Top scores
        scores = top_scores(5)
        y = 220
        self.screen.blit(self.font.render("Top Scores:", True, TEXT), (WIDTH//2 - 80, y - 32))
        for i, (name, pts) in enumerate(scores, start=1):
            line = self.font.render(f"{i:>2}. {name:12s}  {pts}", True, TEXT)
            self.screen.blit(line, (WIDTH//2 - 120, y + (i-1) * 28))

    def draw_game_over(self):
        self.draw_world()
        over = self.big.render("GAME OVER", True, (255, 120, 120))
        self.screen.blit(over, (WIDTH//2 - over.get_width()//2, 90))

        s1 = self.font.render(f"Your Score: {self.game_over_score}", True, TEXT)
        self.screen.blit(s1, (WIDTH//2 - s1.get_width()//2, 150))

        s2 = self.font.render("Enter Name & Press ENTER to Save", True, TEXT)
        self.screen.blit(s2, (WIDTH//2 - s2.get_width()//2, 190))

        entry_box = pygame.Rect(WIDTH//2 - 180, 230, 360, 40)
        pygame.draw.rect(self.screen, (70, 70, 95), entry_box, border_radius=8)
        name_text = self.font.render(self.name_input or "Player", True, (255, 255, 255))
        self.screen.blit(name_text, (entry_box.x + 10, entry_box.y + 8))

        s3 = self.font.render("Press R to restart • Esc for menu", True, TEXT)
        self.screen.blit(s3, (WIDTH//2 - s3.get_width()//2, 290))

    # ---------------- event handling ----------------
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == STATE_MENU:
                if e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_SPACE, pygame.K_UP):
                        self.reset_run()
                        self.state = STATE_PLAY
                    elif e.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

            elif self.state == STATE_PLAY:
                if e.type == pygame.KEYDOWN:
                    if e.key in (pygame.K_SPACE, pygame.K_UP):
                        self.player.jump()
                    elif e.key == pygame.K_ESCAPE:
                        self.reset_run()
                        self.state = STATE_MENU

            elif self.state == STATE_GAME_OVER:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        add_score(self.name_input or "Player", self.game_over_score)
                        self.reset_run()
                        self.state = STATE_MENU
                    elif e.key == pygame.K_BACKSPACE:
                        self.name_input = self.name_input[:-1]
                    elif e.key == pygame.K_r:
                        self.reset_run()
                        self.state = STATE_PLAY
                    elif e.key == pygame.K_ESCAPE:
                        self.reset_run()
                        self.state = STATE_MENU
                    else:
                        if len(self.name_input) < 16:
                            ch = e.unicode
                            if ch.isprintable() and not ch.isspace():
                                self.name_input += ch

    # ---------------- main loop ----------------
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()

            if self.state == STATE_PLAY:
                self.update_play(dt)
                self.draw_world()
                self.draw_hud()
            elif self.state == STATE_MENU:
                self.update_menu(dt)
                self.draw_menu()
            elif self.state == STATE_GAME_OVER:
                self.draw_game_over()

            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
