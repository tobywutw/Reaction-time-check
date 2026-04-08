import pygame
import random
import time
pygame.init()
#自主學習抱歉程式碼可能有點亂
WIDTH = 800
HEIGHT = 600
FPS = 67
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
RED = (255, 0, 0)
BLUE = (0, 102, 204)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("反應時間測試")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("Microsoft JhengHei", 80)
font_large = pygame.font.SysFont("Microsoft JhengHei", 60)
font_medium = pygame.font.SysFont("Microsoft JhengHei", 40)
font_small = pygame.font.SysFont("Microsoft JhengHei", 30)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False
    def draw(self, surface):
        button_color = self.color if not self.hovered else tuple(min(c + 30, 255) for c in self.color)
        pygame.draw.rect(surface, button_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 3)
        text_surface = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)
class GameState:
    def __init__(self):
        self.state = "menu"  
        self.reaction_time = 0
        self.start_countdown = 0
        self.ready_time = 0
        self.wait_duration = random.uniform(2, 5)
        self.waiting_since = 0
    def reset(self):
        self.reaction_time = 0
        self.ready_time = 0
        self.wait_duration = random.uniform(2, 5)
        self.waiting_since = 0
game = GameState()
start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60, "START", GREEN, WHITE)
continue_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 60, "繼續測試", BLUE, WHITE)
running = True
while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()
    start_button.update(mouse_pos)
    continue_button.update(mouse_pos)
    
    # ===== 事件處理 =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                if game.state == "menu":
                    if start_button.is_clicked(mouse_pos):
                        game.state = "countdown"
                        game.start_countdown = time.time()
                
                elif game.state == "waiting":
                    game.state = "result"
                    game.reaction_time = -1
                
                elif game.state == "ready":
                    game.reaction_time = (time.time() - game.ready_time) * 1000
                    game.state = "result"
                
                elif game.state == "result":
                    if continue_button.is_clicked(mouse_pos):
                        game.reset()
                        game.state = "countdown"
                        game.start_countdown = time.time()
    if game.state == "countdown":
        elapsed = time.time() - game.start_countdown
        if elapsed >= 3:
            game.state = "waiting"
            game.waiting_since = time.time()
        countdown_num = int(3 - elapsed) + 1
    
    elif game.state == "waiting":
        elapsed = time.time() - game.waiting_since
        if elapsed >= game.wait_duration:
            game.state = "ready"
            game.ready_time = time.time()
    screen.fill(WHITE)
    if game.state == "menu":
        title = font_title.render("反應時間測試", True, BLUE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
        
        subtitle = font_medium.render("測試你的反應速度", True, BLACK)
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 200))
        
        hint = font_small.render("在綠色出現時立即點擊", True, GRAY)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 280))
        
        start_button.draw(screen)
    elif game.state == "countdown":
        countdown_text = font_title.render(str(countdown_num), True, RED)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - 100))
        
        ready_text = font_medium.render("準備好...", True, BLACK)
        screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2, HEIGHT // 2 + 100))    
    elif game.state == "waiting":
        wait_text = font_large.render("等待中...", True, YELLOW)
        screen.blit(wait_text, (WIDTH // 2 - wait_text.get_width() // 2, HEIGHT // 2 - 80))
        
        hint = font_small.render("不要點擊！等綠色出現", True, BLACK)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 100))
    elif game.state == "ready":
        screen.fill(GREEN)
        ready_text = font_title.render("現在點擊！", True, WHITE)
        screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2, HEIGHT // 2 - 100))
    elif game.state == "result":
        if game.reaction_time == -1:
            screen.fill(RED)
            result_text = font_large.render("太早點擊了！", True, WHITE)
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 120))
        else:
            result_text = font_large.render(f"{game.reaction_time:.0f} ms", True, GREEN)
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 120))
            performance = font_small.render("反應時間", True, BLACK)
            screen.blit(performance, (WIDTH // 2 - performance.get_width() // 2, HEIGHT // 2 + 50))
        continue_button.draw(screen)
    pygame.display.flip()
pygame.quit()
print("感謝遊玩！")
