import pygame
pygame.init()

# Screen Dimensions #
'''
ar in this scenario stands for Aspect Ratio
arW = Aspect Ratio Width
arH = Aspect Ratio Height
arM = Aspect Ratio Multiplier
- This means if at 16:9 and an 80 multiplier the window will be at a 720p resolution at 120 you are at 1080p
'''
arW = 16
arH = 9
arM = 100

screenW = arW * arM
screenH = arH * arM

screen = pygame.display.set_mode((screenW , screenH))

# Time is really important so let's keep a variable that holds the Clock function #
clock = pygame.time.Clock()

# This may go into its own class for dealing with text but for now I'm putting it here since this is just a template #
font = pygame.font.SysFont("Arial",20)
message = None

#Temp Variables for the player
player_x = 0
player_y = 0

# Temporary object in the world
obj_x = 200
obj_y = 150
obj_color = (0, 200, 100)
obj_size = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # MAIN GAME LOOP
    # 1 Time
    dt = clock.tick(60) / (1000/60)
    '''
    You could write it like clock.tick(60) / 16.67 but I want to show you what 16.67 is
    1000ms / 60fps is another way of saying our target speed
    if it's perfect dt will equal 1, if it's slow like lets say 30fps dt will equal 2
    if it runs faster dt / 1.0 the clock.tick function ensures we stay at just 60fps
    Later if we wanted to ensure smoothness and account for any dips in framerate this is important
    to ensure that objects respect time. For example if you were playing a multiplayer game and someone
    was on slow or bad hardware what would happen?
    '''

    # 2 Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= 1
    if keys[pygame.K_RIGHT]:
        player_x += 1
    if keys[pygame.K_LEFT]:
        player_x -= 1
    if keys[pygame.K_DOWN]:
        player_y += 1

    # 3 Physics

    # 4 Update Coordinates

    # 5 Handle Interactions

    # 6 Camera

    # 7 Draw (Paint your pixels each frame)
    screen.fill((0,0,0))

    message = f"PlayerX: {player_x:.2f}  PlayerY: {player_y:.2f}"
    text_surface = font.render(message, True, (255, 255, 255))
    screen.blit(text_surface, (20, 20))

    #temp player object
    pygame.draw.polygon(
        screen,
        (50, 0, 50),
        [
            (screenW / 2, screenH / 2 - 10),
            (screenW / 2 - 10, screenH / 2 + 10),
            (screenW / 2 + 10, screenH / 2 + 10)
        ]
    )

    #temp general object
    pygame.draw.rect(
        screen,
        obj_color,
        (obj_x - player_x, obj_y - player_y, obj_size, obj_size)
    )

    pygame.display.flip()