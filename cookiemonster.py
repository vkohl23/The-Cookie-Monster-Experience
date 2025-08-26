import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CookieMonster")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and resize images
boy_img = pygame.image.load("boy.png")
boy_img = pygame.transform.scale(boy_img, (40, 40))

cookie_img = pygame.image.load("cookie.jpg")
cookie_img = pygame.transform.scale(cookie_img, (25, 25))

broccoli_img = pygame.image.load("broccoli.png")
broccoli_img = pygame.transform.scale(broccoli_img, (30, 30))

# Player class
class Player:
    def __init__(self):
        self.image = boy_img
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 5
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.move_up = True
            if event.key == pygame.K_s:
                self.move_down = True
            if event.key == pygame.K_a:
                self.move_left = True
            if event.key == pygame.K_d:
                self.move_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.move_up = False
            if event.key == pygame.K_s:
                self.move_down = False
            if event.key == pygame.K_a:
                self.move_left = False
            if event.key == pygame.K_d:
                self.move_right = False

    def move(self):
        if self.move_up and self.rect.top > 0:
            self.rect.y -= self.speed
        if self.move_down and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if self.move_left and self.rect.left > 0:
            self.rect.x -= self.speed
        if self.move_right and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, win):
        win.blit(self.image, self.rect)

# Cookie class
class Cookie:
    def __init__(self):
        self.image = cookie_img
        x = random.randint(30, WIDTH-30)
        y = random.randint(30, HEIGHT-30)
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, win):
        win.blit(self.image, self.rect)

# Broccoli class
class Broccoli:
    def __init__(self):
        self.image = broccoli_img
        x = random.randint(50, WIDTH-50)
        y = random.randint(50, HEIGHT-50)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])

    def move(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dir_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dir_y *= -1

    def draw(self, win):
        win.blit(self.image, self.rect)

# Draw text on screen
def draw_text(win, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont("comicsans", size)
    label = font.render(text, True, color)
    win.blit(label, (x, y))

def game_loop():
    clock = pygame.time.Clock()
    player = Player()
    cookies = [Cookie() for _ in range(6)]
    broccolis = [Broccoli() for _ in range(3)]
    score = 0
    game_over = False
    run = True

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if not game_over:
                player.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    return  # Exit to restart

        if not game_over:
            player.move()

            # Check cookie collision
            for cookie in cookies[:]:
                if player.rect.colliderect(cookie.rect):
                    cookies.remove(cookie)
                    score += 10
                    cookies.append(Cookie())

            # Broccoli movement and collision
            for broccoli in broccolis:
                broccoli.move()
                if player.rect.colliderect(broccoli.rect):
                    game_over = True

        # Drawing
        player.draw(WIN)
        for cookie in cookies:
            cookie.draw(WIN)
        for broccoli in broccolis:
            broccoli.draw(WIN)

        # Display score and game over status
        draw_text(WIN, f"Score: {score}", 36, 10, 10)
        if game_over:
            draw_text(WIN, "GAME OVER! Press R to Restart", 48, WIDTH//6, HEIGHT//2, (255, 0, 0))

        pygame.display.update()

def main():
    while True:
        game_loop()

if __name__ == "__main__":
    main()

