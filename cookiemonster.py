import pygame
import random
import sys
import os
import math
import pickle

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = 40
COOKIE_SIZE = 25
BROCCOLI_SIZE = 30
NUM_COOKIES = 8
NUM_BROCCOLIS = 4
SAFE_RADIUS = 120  
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CookieMonster Open World")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 120, 255)


def load_image(name, size):
    try:
        img = pygame.image.load(name)
        return pygame.transform.scale(img, size)
    except Exception:
        surf = pygame.Surface(size)
        surf.fill(YELLOW)
        return surf

boy_img = load_image("boy.png", (PLAYER_SIZE, PLAYER_SIZE))
cookie_img = load_image("cookie.jpg", (COOKIE_SIZE, COOKIE_SIZE))
broccoli_img = load_image("broccoli.png", (BROCCOLI_SIZE, BROCCOLI_SIZE))

def load_sound(name):
    try:
        return pygame.mixer.Sound(name)
    except Exception:
        return None

eat_sound = load_sound("eat.wav")
lose_sound = load_sound("lose.wav")


def draw_text(win, text, size, x, y, color=WHITE, center=False):
    font = pygame.font.SysFont("comicsans", size)
    label = font.render(text, True, color)
    if center:
        rect = label.get_rect(center=(x, y))
        win.blit(label, rect)
    else:
        win.blit(label, (x, y))

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def save_score(score):
    try:
        with open("score.dat", "wb") as f:
            pickle.dump(score, f)
    except Exception:
        pass

def load_score():
    try:
        with open("score.dat", "rb") as f:
            return pickle.load(f)
    except Exception:
        return 0

class Player:
    def __init__(self):
        self.image = boy_img
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 5
        self.dx = 0
        self.dy = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP): self.dy = -self.speed
            if event.key in (pygame.K_s, pygame.K_DOWN): self.dy = self.speed
            if event.key in (pygame.K_a, pygame.K_LEFT): self.dx = -self.speed
            if event.key in (pygame.K_d, pygame.K_RIGHT): self.dx = self.speed
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN): self.dy = 0
            if event.key in (pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT): self.dx = 0

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, win):
        win.blit(self.image, self.rect)

class Cookie:
    def __init__(self, player_rect):
        while True:
            x = random.randint(COOKIE_SIZE, WIDTH-COOKIE_SIZE)
            y = random.randint(COOKIE_SIZE, HEIGHT-COOKIE_SIZE)
            if distance((x, y), player_rect.center) > SAFE_RADIUS:
                break
        self.image = cookie_img
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, win):
        win.blit(self.image, self.rect)

SAFE_RADIUS = 40  

class Broccoli:
    def __init__(self, player_rect):
        while True:
            x = random.randint(BROCCOLI_SIZE, WIDTH-BROCCOLI_SIZE)
            y = random.randint(BROCCOLI_SIZE, HEIGHT-BROCCOLI_SIZE)
            if distance((x, y), player_rect.center) > SAFE_RADIUS:
                break
        self.image = broccoli_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 4)
        self.angle = random.uniform(0, 2*math.pi)

    def move(self):
        self.rect.x += int(math.cos(self.angle) * self.speed)
        self.rect.y += int(math.sin(self.angle) * self.speed)
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.angle = math.pi - self.angle + random.uniform(-0.2, 0.2)
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.angle = -self.angle + random.uniform(-0.2, 0.2)
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, win):
        win.blit(self.image, self.rect)



class Game:
    def __init__(self):
        self.state = "menu"
        self.player = Player()
        self.cookies = []
        self.broccolis = []
        self.score = 0
        self.high_score = load_score()
        self.paused = False
        self.last_broccoli_spawn = pygame.time.get_ticks()

    def reset(self):
        self.player = Player()
        self.cookies = [Cookie(self.player.rect) for _ in range(NUM_COOKIES)]
        self.broccolis = [Broccoli(self.player.rect) for _ in range(NUM_BROCCOLIS)]
        self.score = 0
        self.paused = False
        self.last_broccoli_spawn = pygame.time.get_ticks()

    def update(self):
        self.player.move()
        
        for cookie in self.cookies[:]:
            if self.player.rect.colliderect(cookie.rect):
                self.cookies.remove(cookie)
                self.score += 10
                if eat_sound: eat_sound.play()
                self.cookies.append(Cookie(self.player.rect))
        
        for broccoli in self.broccolis:
            broccoli.move()
            if self.player.rect.colliderect(broccoli.rect):
                if lose_sound: lose_sound.play()
                self.state = "gameover"
                if self.score > self.high_score:
                    self.high_score = self.score
                    save_score(self.high_score)
        
        now = pygame.time.get_ticks()
        if now - self.last_broccoli_spawn > 8000:
            self.broccolis.extend([Broccoli(self.player.rect) for _ in range(2)])
            self.last_broccoli_spawn = now


class Game:
    def __init__(self):
        self.state = "menu"
        self.player = Player()
        self.cookies = []
        self.broccolis = []
        self.score = 0
        self.high_score = load_score()
        self.paused = False

    def reset(self):
        self.player = Player()
        self.cookies = [Cookie(self.player.rect) for _ in range(NUM_COOKIES)]
        self.broccolis = [Broccoli(self.player.rect) for _ in range(NUM_BROCCOLIS)]
        self.score = 0
        self.paused = False

    def run(self):
        self.reset()
        while True:
            clock.tick(FPS)
            WIN.fill(BLACK)
            if self.state == "menu":
                self.draw_menu()
                self.handle_menu_events()
            elif self.state == "playing":
                self.handle_events()
                if not self.paused:
                    self.update()
                self.draw()
            elif self.state == "gameover":
                self.draw_gameover()
                self.handle_gameover_events()
            pygame.display.update()

    def draw_menu(self):
        draw_text(WIN, "COOKIE MONSTER", 64, WIDTH//2, HEIGHT//4, YELLOW, center=True)
        draw_text(WIN, "Press SPACE to Start", 36, WIDTH//2, HEIGHT//2, WHITE, center=True)
        draw_text(WIN, f"High Score: {self.high_score}", 32, WIDTH//2, HEIGHT//2+60, GREEN, center=True)
        draw_text(WIN, "WASD or Arrow keys to move", 24, WIDTH//2, HEIGHT//2+120, BLUE, center=True)

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "playing"
                    self.reset()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                if event.key == pygame.K_r and self.state == "playing":
                    self.reset()
            self.player.handle_event(event)

    def update(self):
        self.player.move()
       
        for cookie in self.cookies[:]:
            if self.player.rect.colliderect(cookie.rect):
                self.cookies.remove(cookie)
                self.score += 10
                if eat_sound: eat_sound.play()
                self.cookies.append(Cookie(self.player.rect))
      
        for broccoli in self.broccolis:
            broccoli.move()
            if self.player.rect.colliderect(broccoli.rect):
                if lose_sound: lose_sound.play()
                self.state = "gameover"
                if self.score > self.high_score:
                    self.high_score = self.score
                    save_score(self.high_score)

    def draw(self):
        self.player.draw(WIN)
        for cookie in self.cookies:
            cookie.draw(WIN)
        for broccoli in self.broccolis:
            broccoli.draw(WIN)
        draw_text(WIN, f"Score: {self.score}", 32, 10, 10, WHITE)
        draw_text(WIN, f"High Score: {self.high_score}", 24, 10, 40, GREEN)
        if self.paused:
            draw_text(WIN, "PAUSED", 48, WIDTH//2, HEIGHT//2, RED, center=True)

    def draw_gameover(self):
        WIN.fill(BLACK)
        draw_text(WIN, "GAME OVER!", 64, WIDTH//2, HEIGHT//3, RED, center=True)
        draw_text(WIN, f"Score: {self.score}", 36, WIDTH//2, HEIGHT//2, WHITE, center=True)
        draw_text(WIN, f"High Score: {self.high_score}", 32, WIDTH//2, HEIGHT//2+40, GREEN, center=True)
        draw_text(WIN, "Press R to Restart or ESC for Menu", 28, WIDTH//2, HEIGHT//2+100, YELLOW, center=True)

    def handle_gameover_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = "playing"
                    self.reset()
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"


if __name__ == "__main__":
    Game().run()
