import pygame
from settings import FONT_NAME, FONT_SIZE, FONT_BIG, TEXT, ACCENT
from db import best_score, top_scores

class UI:
    def __init__(self):
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.big = pygame.font.SysFont(FONT_NAME, FONT_BIG, bold=True)

    def draw_score_hud(self, screen, score: int):
        s = self.font.render(f"Score: {score}", True, TEXT)
        b = self.font.render(f"Best: {best_score()}", True, ACCENT)
        screen.blit(s, (20, 16))
        screen.blit(b, (20, 46))

    def draw_menu(self, screen, width, title_y, scores_y):
        title = self.big.render("ENDLESS RUNNER", True, ACCENT)
        screen.blit(title, (width//2 - title.get_width()//2, title_y))
        tip = self.font.render("Press SPACE to Start • Esc to Quit", True, TEXT)
        screen.blit(tip, (width//2 - tip.get_width()//2, title_y + 60))
        scores = top_scores(5)
        y = scores_y
        screen.blit(self.font.render("Top Scores:", True, TEXT), (width//2 - 80, y - 32))
        for i, (name, pts) in enumerate(scores, start=1):
            line = self.font.render(f"{i:>2}. {name:12s}  {pts}", True, TEXT)
            screen.blit(line, (width//2 - 120, y + (i-1) * 28))

    def draw_game_over(self, screen, width, score, name_input):
        over = self.big.render("GAME OVER", True, (255, 120, 120))
        screen.blit(over, (width//2 - over.get_width()//2, 90))
        s1 = self.font.render(f"Your Score: {score}", True, TEXT)
        screen.blit(s1, (width//2 - s1.get_width()//2, 150))
        s2 = self.font.render("Enter Name & Press ENTER to Save", True, TEXT)
        screen.blit(s2, (width//2 - s2.get_width()//2, 190))
        entry_box = pygame.Rect(width//2 - 180, 230, 360, 40)
        pygame.draw.rect(screen, (70, 70, 95), entry_box, border_radius=8)
        name_text = self.font.render(name_input or "Player", True, (255, 255, 255))
        screen.blit(name_text, (entry_box.x + 10, entry_box.y + 8))
        s3 = self.font.render("Press R to restart • Esc for menu", True, TEXT)
        screen.blit(s3, (width//2 - s3.get_width()//2, 290))
