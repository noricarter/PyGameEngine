import sys
import pygame

from settings import WIDTH, HEIGHT, FPS, PLAYER_H, GROUND_Y
from states import STATE_MENU, STATE_PLAY, STATE_GAME_OVER
from entities import Player
from world import World
from ui import UI
from db import add_score

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Endless Runner • Pygame + SQLite")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.ui = UI()
        self.world = World()

        self.state = STATE_MENU
        self.name_input = ""
        self.game_over_score = 0
        # NOTE: use PLAYER_H here (small bugfix from earlier draft)
        self.player = Player(120, GROUND_Y - PLAYER_H)

    # --- lifecycle helpers ---
    def reset_run(self):
        self.world.reset()
        self.player = Player(120, GROUND_Y - PLAYER_H)
        self.game_over_score = 0

    # --- event handling ---
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

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

    # --- update/draw per-state ---
    def update_menu(self, dt: float):
        # Player idle on the ground; world stays idle
        self.player.y = GROUND_Y - PLAYER_H
        self.player.vy = 0
        self.player.on_ground = True
        self.world.update_menu(dt)

    def update_play(self, dt: float):
        self.player.update()
        self.world.update_play(dt)
        # Collision check
        pr = self.player.rect()
        for ob in self.world.obstacles:
            if pr.colliderect(ob.rect()):
                self.state = STATE_GAME_OVER
                self.game_over_score = int(self.world.distance // 5)
                self.name_input = ""
                break

    def draw_world(self):
        self.world.draw_background(self.screen)
        self.world.draw_obstacles(self.screen)
        self.player.draw(self.screen)

    def draw_menu(self):
        self.draw_world()
        self.ui.draw_menu(self.screen, WIDTH, 90, 220)

    def draw_play(self):
        self.draw_world()
        score = int(self.world.distance // 5)
        self.ui.draw_score_hud(self.screen, score)

    def draw_game_over(self):
        self.draw_world()
        self.ui.draw_game_over(self.screen, WIDTH, self.game_over_score, self.name_input)

    # --- main loop ---
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()

            if self.state == STATE_MENU:
                self.update_menu(dt)
                self.draw_menu()
            elif self.state == STATE_PLAY:
                self.update_play(dt)
                self.draw_play()
            elif self.state == STATE_GAME_OVER:
                self.draw_game_over()

            pygame.display.flip()
