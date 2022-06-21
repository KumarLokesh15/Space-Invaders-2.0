import pygame
import random
import math
from pygame import mixer
import time

# initialize the pygame
pygame.init()

# create the screeen
screenW, screenH = 1280, 720
screen = pygame.display.set_mode((1280, 720))

# background
background = pygame.image.load("images/bg.jpg")

# background music
mixer.music.load("music/bg2.mp3")
mixer.music.play(-1)

# Title & icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/player_1.png")
pygame.display.set_icon(icon)

# game start
timeStart = time.time()
totalWaitingTime = 4
game_start = 0
start_font = pygame.font.Font("font/OriginTech personal use.ttf", 110)
start_text = start_font.render("SPACE INVADERS 2.0", True, (255, 255, 255))

if time.time() - timeStart <= totalWaitingTime:
    while time.time() - timeStart <= totalWaitingTime:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        screen.blit(start_text, (60, 300))
        pygame.display.update()

# player
playerImg = pygame.image.load("images/player_1.png")
playerX = (screenW - 64) // 2
playerY = 600
playerX_change = 0
playerY_change = 0

# enemy
# enemyImg = pygame.image.load('images/enemy_3.png')
# enemyX = random.randint(0,screenW)
# enemyY = random.randint(0,600)
# enemyX_change = 2
# enemyY_change = 2

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("images/enemy_1.png"))
    enemyX.append(random.randint(0, screenW))
    enemyY.append(random.randint(0, 600))
    enemyX_change.append(1)
    enemyY_change.append(1)

# bullet
# ready - can't see the bullet on the screen
# fire - bullet is currently moving
bulletImg = pygame.image.load("images/bullet_1.png")
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

score_val = 0
font = pygame.font.Font("freesansbold.ttf", 64)
textX, textY = 10, 10

# Game Over text
# over_font = pygame.font.Font('freesansbold.ttf',128)
# over_font = pygame.font.Font('font/batmfa__.ttf',128)
over_font = pygame.font.Font("font/OriginTech personal use.ttf", 128)
# over_font = pygame.font.Font('font/space age.ttf',128)


def show_score(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (240, 300))


# Draw player
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# def enemy(x,y):
#     screen.blit(enemyImg,(x,y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision_Bullet(eX, eY, bX, bY):
    distance = math.sqrt((math.pow(eX - bX, 2)) + (math.pow(eY - bY, 2)))
    if distance < 27:
        return 1
    else:
        return 0


global collision_flag
collision_flag = 0


def isCollision_Rocket(eX, eY, pX, pY):
    distance = math.sqrt((math.pow(eX - pX, 2)) + (math.pow(eY - pY, 2)))
    if distance < 100:
        return 1
    else:
        return 0


# Game Loop
running = 1
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0

        # if key stroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            # print("Key stroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change -= 2
            elif event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                playerX_change += 2
            elif event.key == pygame.K_UP:
                playerY_change -= 2
            elif event.key == pygame.K_DOWN:
                playerY_change += 2
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("music/laser.wav")
                    bullet_Sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if (
                event.key == pygame.K_LEFT
                or event.key == pygame.K_RIGHT
                or event.key == pygame.K_UP
                or event.key == pygame.K_DOWN
            ):
                # print("Key stroke has been released")
                playerX_change = 0
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= screenW - 64:
        playerX = screenW - 64

    if playerY <= 0:
        playerY = 0
    elif playerY >= 656:
        playerY = 656

    if collision_flag:
        game_over_text()
        # collision_Bullet = 0

    else:
        for i in range(no_of_enemies):
            collision_Bullet = isCollision_Bullet(
                enemyX[i], enemyY[i], bulletX, bulletY
            )
            collision_Rocket = isCollision_Bullet(
                enemyX[i], enemyY[i], playerX, playerY
            )
            if collision_Rocket and not collision_flag:
                explosion_Sound = mixer.Sound("music/explosion.wav")
                explosion_Sound.play()
                collision_flag = 1

            if not collision_flag:
                if enemyX[i] <= 0:
                    enemyX_change[i] = 1
                elif enemyX[i] >= screenW - 64:
                    enemyX_change[i] = -1

                if enemyY[i] <= 0:
                    enemyY_change[i] = 1
                elif enemyY[i] >= 656:
                    enemyY_change[i] = -1

                enemyX[i] += enemyX_change[i]
                enemyY[i] += enemyY_change[i]

                # Collision
                if collision_Bullet:
                    explosion_Sound = mixer.Sound("music/explosion.wav")
                    explosion_Sound.play()
                    bulletY = playerY
                    bullet_state = "ready"
                    score_val += 1
                    print(score_val)
                    enemyX[i] = random.randint(0, screenW - 64)
                    enemyY[i] = random.randint(0, 600)

                enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
