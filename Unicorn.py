import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Anežka design studio: Jednorožec a diamanty")

# Colors
WHITE = (255, 255, 255)

def show_start_menu():
    start_font = pygame.font.Font(None, 72)
    start_text = start_font.render("Press SPACE to Start", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
    return True

def show_game_over(message):
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render(message, True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before closing

if not show_start_menu():
    running = False
else:
    running = True

start_time = pygame.time.get_ticks()
time_limit = 90000  # 90 seconds

# Load images
background = pygame.image.load("background.png")
unicorn_img = pygame.image.load("unicorn.png")
pink_donut_img = pygame.image.load("pink_donut.png")
green_donut_img = pygame.image.load("green_donut.png")

# Unicorn properties
unicorn_width = 128
unicorn_height = 128
unicorn_x = (SCREEN_WIDTH - unicorn_width) // 3
unicorn_y = SCREEN_HEIGHT - unicorn_height - 1
unicorn_speed = 10

# Donut properties
donut_width = 40
donut_height = 40
donut_speed = 5
donuts = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

def draw_unicorn(x, y):
    screen.blit(unicorn_img, (x, y))

def draw_donut(x, y, color):
    if color == "pink":
        screen.blit(pink_donut_img, (x, y))
    elif color == "green":
        screen.blit(green_donut_img, (x, y))

def create_donut():
    x = random.randint(0, SCREEN_WIDTH - donut_width)
    y = 0
    color = random.choice(["pink", "green"])
    donuts.append({"x": x, "y": y, "color": color})

def update_donuts():
    for donut in donuts[:]:
        donut["y"] += donut_speed
        if donut["y"] > SCREEN_HEIGHT:
            donuts.remove(donut)

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def check_collision():
    global score
    for donut in donuts[:]:
        if (unicorn_x < donut["x"] + donut_width and
            unicorn_x + unicorn_width > donut["x"] and
            unicorn_y < donut["y"] + donut_height and
            unicorn_y + unicorn_height > donut["y"]):
            if donut["color"] == "pink":
                score += 1
            else:
                score -= 1
            donuts.remove(donut)

# Game loop
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and unicorn_x > 0:
        unicorn_x -= unicorn_speed
    if keys[pygame.K_RIGHT] and unicorn_x < SCREEN_WIDTH - unicorn_width:
        unicorn_x += unicorn_speed

    if random.randint(1, 20) == 1:
        create_donut()

    update_donuts()
    check_collision()

    for donut in donuts:
        draw_donut(donut["x"], donut["y"], donut["color"])

    draw_unicorn(unicorn_x, unicorn_y)
    draw_score()

    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time >= time_limit:
        show_game_over("Time is over!")
        running = False

    if score >= 35:
        show_game_over("You win!")
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
