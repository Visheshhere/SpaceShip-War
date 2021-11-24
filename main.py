import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Ship WAR")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

DIVIDER = pygame.Rect(WIDTH // 2 - 4, 0, 10, HEIGHT)

MENU_FONT = pygame.font.SysFont('georgia', 70)
MENU_FONT2 = pygame.font.SysFont('georgia', 40)
CONTROL_FONT = pygame.font.SysFont('arial', 20)
HEALTH_FONT = pygame.font.SysFont('comicsams', 40)
WINNER_FONT = pygame.font.SysFont('comicsams', 100)
CREDIT = pygame.font.SysFont('Mistral', 26)

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_YELLOW_BULLETS = 5
MAX_RED_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_COLLIDE = pygame.USEREVENT + 1
RED_COLLIDE = pygame.USEREVENT + 2
Y_HEALTH_HIT = pygame.USEREVENT + 3
R_HEALTH_HIT = pygame.USEREVENT + 4

YELLOW_SPACESHIP_IMAGE = pygame.image.load("resources/yellow_ship.jpg")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load("resources/red_ship.jpg")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BACKGROUND = pygame.transform.scale(pygame.image.load("resources/background.jpg"), (WIDTH, HEIGHT))

HEALTH_IMAGE = pygame.transform.scale(pygame.image.load("resources/health.png"), (40, 40))
MENU_IMAGE = pygame.transform.scale(pygame.image.load("resources/menu background.jpg"), (WIDTH, HEIGHT + 20))
CONTROLS_IMAGE = pygame.transform.scale(pygame.image.load("resources/Controls.jpg"), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, health):
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, DIVIDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    WINDOW.blit(HEALTH_IMAGE, (health.x, health.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def yellow_ship_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < DIVIDER.x:  # RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT:  # DOWN
        yellow.y += VELOCITY


def red_ship_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > DIVIDER.x + DIVIDER.width:  # LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:  # RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # UP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT:  # DOWN
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red, health_buff):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_COLLIDE))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        elif health_buff.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Y_HEALTH_HIT))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_COLLIDE))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        elif health_buff.colliderect(bullet):
            pygame.event.post(pygame.event.Event(R_HEALTH_HIT))
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /
                            2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    return False
                    main_menu()
        pygame.display.update()


def controls():
    while True:
        WINDOW.blit(CONTROLS_IMAGE, (0, 0))
        player1 = MENU_FONT2.render(" PLAYER 1 ", 1, YELLOW)
        up1 = CONTROL_FONT.render(" UP    :    W", 1, WHITE)
        down1 = CONTROL_FONT.render(" DOWN    :    S", 1, WHITE)
        left1 = CONTROL_FONT.render(" LEFT   :   A", 1, WHITE)
        right1 = CONTROL_FONT.render(" RIGHT   :   D ", 1, WHITE)
        player2 = MENU_FONT2.render(" PLAYER 2 ", 1, RED)
        up2 = CONTROL_FONT.render(" UP   :   Up Arrow Key ", 1, WHITE)
        down2 = CONTROL_FONT.render(" DOWN   :   Down Arrow Key ", 1, WHITE)
        left2 = CONTROL_FONT.render(" LEFT   :   Left Arrow Key ", 1, WHITE)
        right2 = CONTROL_FONT.render(" RIGHT   :   Right Arrow Key ", 1, WHITE)
        shoot1 = CONTROL_FONT.render(" Shoot   :   Left CTRL ", 1, WHITE)
        shoot2 = CONTROL_FONT.render(" Shoot   :   RIGHT CTRL ", 1, WHITE)

        WINDOW.blit(player1, (WIDTH // 2 - 300, HEIGHT // 2 - 245))
        WINDOW.blit(up1, (WIDTH // 2 - 150, HEIGHT // 2 - 190))
        WINDOW.blit(down1, (WIDTH // 2 - 150, HEIGHT // 2 - 160))
        WINDOW.blit(left1, (WIDTH // 2 - 150, HEIGHT // 2 - 130))
        WINDOW.blit(right1, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        WINDOW.blit(shoot1, (WIDTH // 2 - 150, HEIGHT // 2 - 70))
        WINDOW.blit(player2, (WIDTH // 2 - 300, HEIGHT // 2 - 20))
        WINDOW.blit(up2, (WIDTH // 2 - 150, HEIGHT // 2 + 40))
        WINDOW.blit(down2, (WIDTH // 2 - 150, HEIGHT // 2 + 70))
        WINDOW.blit(left2, (WIDTH // 2 - 150, HEIGHT // 2 + 100))
        WINDOW.blit(right2, (WIDTH // 2 - 150, HEIGHT // 2 + 130))
        WINDOW.blit(shoot2, (WIDTH // 2 - 150, HEIGHT // 2 + 160))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                    main_menu()

        pygame.display.update()


def main_menu():
    flag = 0
    while True:
        WINDOW.blit(MENU_IMAGE, (0, 0))
        menu = MENU_FONT.render(" SpaceShip War  ", 1, WHITE)
        vishesh = CREDIT.render(" BY VISHESH  ", 1, BLACK)

        if flag == 0:
            start = MENU_FONT2.render(" START GAME ", 1, RED)
            control = MENU_FONT2.render(" CONTROLS ", 1,  WHITE)
            quit = MENU_FONT2.render(" QUIT ", 1, WHITE)

        elif flag == 1:
            start = MENU_FONT2.render(" START GAME ", 1, WHITE)
            control = MENU_FONT2.render(" CONTROLS ", 1, RED)
            quit = MENU_FONT2.render(" QUIT ", 1, WHITE)

        elif flag == 2:
            start = MENU_FONT2.render(" START GAME ", 1, WHITE)
            control = MENU_FONT2.render(" CONTROLS ", 1, WHITE)
            quit = MENU_FONT2.render(" QUIT ", 1, RED)

        WINDOW.blit(menu, (WIDTH // 2 - 300, HEIGHT // 2 - 200))
        WINDOW.blit(vishesh, (WIDTH // 2 + 60, HEIGHT // 2 - 125))
        WINDOW.blit(start, (WIDTH // 2 + 150, HEIGHT // 2 - 50))
        WINDOW.blit(control, (WIDTH // 2 + 150, HEIGHT // 2))
        WINDOW.blit(quit, (WIDTH // 2 + 150, HEIGHT // 2 + 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_UP:
                    if flag>0 and flag<=2:
                        flag -= 1
                elif event.key == pygame.K_DOWN:
                    if flag>=0 and flag<2:
                        flag += 1
                elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                elif event.key == pygame.K_RETURN:
                    if flag == 0:
                        return True
                    if flag == 1:
                        controls()
                    if flag == 2:
                        pygame.quit()

        pygame.display.update()


def main():
    red = pygame.Rect(800, 250, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    yellow = pygame.Rect(150, 250, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    health = pygame.Rect(random.randint(200, 800), random.randint(50, 550), SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    main_menu()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_YELLOW_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 - 1, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_RED_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2 - 1, 10, 5)
                    red_bullets.append(bullet)

                if event.key == pygame.K_ESCAPE:
                    yellow_health = 10
                    red_health = 10
                    main_menu()

            if event.type == RED_COLLIDE:
                red_health -= 1

            if event.type == YELLOW_COLLIDE:
                yellow_health -= 1

            if event.type == Y_HEALTH_HIT:
                health = pygame.Rect(random.randint(200, 700), random.randint(50, 450), SPACESHIP_WIDTH,
                                     SPACESHIP_HEIGHT)
                yellow_health +=1

            if event.type == R_HEALTH_HIT:
                health = pygame.Rect(random.randint(200, 700), random.randint(50, 450), SPACESHIP_WIDTH,
                                     SPACESHIP_HEIGHT)
                red_health += 1

        winner_text = ""
        if red_health <= 0:
            WINDOW.blit(BACKGROUND, (0, 0))
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            WINDOW.blit(BACKGROUND, (0, 0))
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_ship_movement(keys_pressed, yellow)
        red_ship_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red, health)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, health)


if __name__ == "__main__":
    main()
