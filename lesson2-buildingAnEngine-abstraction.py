import pygame
from gameObjects2.player import Player
from gameObjects2.controller import Controller
from gameObjects2.camera import Camera
from gameObjects2.world import World

pygame.init()

# Screen Setup
screenW = 16 * 80
screenH = 9 * 80
screen = pygame.display.set_mode((screenW, screenH))
clock = pygame.time.Clock()

# Game Objects
controller = Controller()
player = Player(0, 0, controller)
camera = Camera(screenW, screenH)
square = World(200, 150, 20)

# Font (used for debugging and info display)
font = pygame.font.SysFont("Arial", 20)
message = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # MAIN GAME LOOP
    # 1 Time
    dt = clock.tick(60) / (1000 / 60)

    # 2 Controls

    # 3 Physics
    # (Reserved for gravity, velocity, etc.)

    # 4 Update Coordinates
    player.update(dt)

    # 5 Handle Interactions
    # (Future: collisions, pickups, damage, etc.)

    # 6 Camera
    camera.update(player)

    # 7 Draw (Paint your pixels each frame)
    screen.fill((0, 0, 0))

    # Optional: Print debug info
    message = f"PlayerX: {player.x:.2f}  PlayerY: {player.y:.2f}"
    screen.blit(font.render(message, True, (255, 255, 255)), (20, 20))

    # Draw all game objects
    player.draw(screen, screenW, screenH)
    square.draw(screen, camera)

    pygame.display.flip()
