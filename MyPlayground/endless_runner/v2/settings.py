from pathlib import Path

# Screen / world
WIDTH, HEIGHT = 900, 520
GROUND_Y = HEIGHT - 80
FPS = 60

# Player
PLAYER_W, PLAYER_H = 50, 60
JUMP_VELOCITY = -15.0
GRAVITY = 0.8

# Speed / difficulty
BASE_SPEED = 7.0
SPAWN_COOLDOWN_MIN = 0.65
SPAWN_COOLDOWN_MAX = 1.4

# Obstacles
OB_MIN_W, OB_MAX_W = 30, 60
OB_MIN_H, OB_MAX_H = 30, 80
OB_GAP_MIN = 220

# Colors
BG = (22, 22, 28)
GROUND = (40, 40, 55)
PLAYER_COLOR = (240, 240, 255)
OB_COLOR = (90, 210, 140)
TEXT = (230, 233, 240)
ACCENT = (255, 209, 102)

APP_NAME = "EndlessRunner"
DATA_DIR_HINT = Path.home()  # for non-Windows

# Fonts
FONT_NAME = "consolas"
FONT_SIZE = 26
FONT_BIG = 40
