import pygame
from gameObjects.player import Player
from gameObjects.controller import Controller
from gameObjects.camera import Camera
from gameObjects.world import World
from gameObjects.planet import Planet

pygame.init()

# Screen Setup
screenW = 16 * 80
screenH = 9 * 80
screen = pygame.display.set_mode((screenW, screenH))
clock = pygame.time.Clock()

# Game Objects
controller = Controller()
player = Player(0, 0, controller)
camera = Camera(screenW, screenH, mode="follow", target=player)
world = World()

world.add(camera)

# Example planet (for later physics)
earth = Planet(200, 150, radius=40, color=(0, 120, 255), mass=5000)

# Register objects in the world
world.add(player)
world.add(earth)

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
    controller.update(pygame.key.get_pressed())

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
    world.render(screen, camera)  # camera passed in, not owned by world

    # Optional: Print debug info
    message = f"PlayerX: {player.x:.2f}  PlayerY: {player.y:.2f}"
    screen.blit(font.render(message, True, (255, 255, 255)), (20, 20))

    pygame.display.flip()
