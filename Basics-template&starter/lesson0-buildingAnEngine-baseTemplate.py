import pygame
pygame.init()

screenW = 16*80
screenH = 9*80 #720p in a 16:9 aspect ratio
screen = pygame.display.set_mode((screenW , screenH))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # MAIN GAME LOOP
    # 1 Time

    # 2 Controls

    # 3 Physics

    # 4 Update Coordinates

    # 5 Handle Interactions

    # 6 Camera

    # 7 Draw (Paint your pixels each frame)
    screen.fill((0,0,0))
    pygame.display.flip()