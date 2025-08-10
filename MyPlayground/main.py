import pygame
import time

from gameObject.player import Player
from gameObject.world import World
from gameObject.camera import Camera
from gameObject.platform import Platform

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Arial', 36)
message = 'Something'
text_surface = font.render(message, True, (255, 255, 255))

# Settings
windowed_mode = 1
arW, arH, arM = 16, 9, 100
screenW = arW * arM
screenH = arH * arM

screen = pygame.display.set_mode((screenW, screenH))
clock = pygame.time.Clock()

# Create game objects
player = Player(world_x=0, world_y=screenH-40, radius=10)
world = World(ground_level=screenH-40)
camera = Camera(screenW, screenH)

# Create a test platform
test_platform = Platform(world_x=300, world_y=screenH-120, width=200, height=20)
world.add_platform(test_platform)

running = True
while running:
    dt = clock.tick(60) / 16.67  # delta time (1.0 at 60fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # ESC toggles window/fullscreen
    if keys[pygame.K_ESCAPE]:
        time.sleep(0.2)
        if windowed_mode == 0:
            windowed_mode = 1
            screen = pygame.display.set_mode((screenW, screenH))
        else:
            windowed_mode = 0
            infoObject = pygame.display.Info()
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            screenW, screenH = infoObject.current_w, infoObject.current_h

    # Movement
    player.velocity_x = 0
    if keys[pygame.K_a]:
        player.velocity_x = -2
    if keys[pygame.K_d]:
        player.velocity_x = 2
    if keys[pygame.K_w]:
        player.jump()

    # Update
    ground_y = world.get_ground_height_at(player.world_x, player.world_y, player.velocity_y)
    player.update(ground_y)
    camera.follow_x(player)

    # Draw
    screen.fill((0, 0, 0))
    screen_x, screen_y = camera.world_to_screen(player.world_x, player.world_y)
    pygame.draw.circle(screen, (0, 255, 255), (int(screen_x), int(screen_y)), 10)
    for platform in world.platforms:
        platform.draw(screen, camera)

    # Update and draw the text
    message = f"Player X: {player.world_x:.2f}"
    text_surface = font.render(message, True, (255, 255, 255))
    screen.blit(text_surface, (50, 50))

    pygame.display.flip()