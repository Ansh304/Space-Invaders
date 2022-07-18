import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# creating the window screen( width , height)
screen = pygame.display.set_mode((800, 600))

# create background
background = pygame.image.load('background.jpg')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# creating TITLE
pygame.display.set_caption("SPACE_INVADER")

# creating icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# creating image in screen or player image
player_img = pygame.image.load('003-space-invaders.png')
player_X = 370  # where you want to display
player_Y = 500
player_X_change = 0  # chainging value for moving the player
player_Y_change = 0

# enemy
enemy_img = []
enemy_X = []
enemy_Y = []
enemy_X_change = []
enemy_Y_change = []
no_of_enemy = 6

for i in range(no_of_enemy):
    enemy_img.append(pygame.image.load('enemy.png '))
    enemy_X.append(random.randint(0, 735))
    enemy_Y.append(random.randint(50, 150))
    enemy_Y_change.append(25)
    enemy_X_change.append(2)

# bullet
bullet_img = pygame.image.load('bullet.png')
bullet_X = player_X
bullet_Y = player_Y
bullet_Y_change = 4
bullet_X_change = 0
bullet_state = 'ready'  # state { ready -> you can see the bullet in the screen
# fire -> the bullet is currently moving }

# for counting the score
score_value = 0
font = pygame.font.Font('newfont.ttf', 32)
text_X = 10
text_Y = 10


# for showing the score on screen
def show_score(x, y):
    score = font.render("score " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# for game over text
over = pygame.font.Font('game_over.ttf', 64)


def game_over_text():
    game_over = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


# making the function to show the image of player
def player(x, y):
    screen.blit(player_img, (x, y))


# making the function to show the image of enemy
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# for fire the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x, y - 32))


# for the colision of bullet with enemy
def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 25:
        return True
    else:
        return False

        # **************game loop**************


running = True
while running:

    # for back ground image
    screen.blit(background, (0, 0))

    # for all event in screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking which keystrock is pressed from key borard or checking the key board functnality
        if event.type == pygame.KEYDOWN:  # IT CHECK that key is pressed now
            if event.key == pygame.K_LEFT:  # for preesing left key
                player_X_change = -2  # move left side

            if event.key == pygame.K_RIGHT:  # for preesing right key
                player_X_change = 2  # move right side

            if event.key == pygame.K_SPACE:  # for shoot the bullet
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')  # for producing sound on releasing of bullet
                    bullet_sound.play()
                    bullet_X = player_X
                    fire_bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:  # for releasing key
                player_X_change = 0

    # movement of player
    player_X += player_X_change

    # for restrict the boundries of moving player
    if player_X < 0:
        player_X = 0
    elif player_X > 736:
        player_X = 736

        # enemy movement
    for i in range(no_of_enemy):

        # ***********GAME OVER***********
        if enemy_Y[i] > 450:
            for j in range(no_of_enemy):
                enemy_Y[j] = 2000

            game_over_text()
            break

        enemy_X[i] += enemy_X_change[i]
        if enemy_X[i] <= 0:
            enemy_X_change[i] = 2
            enemy_Y[i] += enemy_Y_change[
                i]  # this line for when enemy touches wall it come downword by 40 or any other we want
        elif enemy_X[i] >= 736:
            enemy_X_change[i] = -2
            enemy_Y[i] += enemy_Y_change[i]

        # collision
        hit = collision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if hit == True:
            bullet_sound = mixer.Sound('explosion.wav')
            bullet_sound.play()
            bullet_Y = player_Y
            bullet_state = 'ready'
            score_value += 1
            enemy_X[i] = random.randint(0, 735)
            enemy_Y[i] = random.randint(50, 150)

        enemy(enemy_X[i], enemy_Y[i], i)

    # bullet movement
    if bullet_Y < 0:
        bullet_state = 'ready'  # for reload the bullet
        bullet_Y = player_Y

    if bullet_state == 'fire':
        bullet_Y -= bullet_Y_change
        fire_bullet(bullet_X, bullet_Y)

    # calling function to showing the  image in screen
    player(player_X, player_Y)
    show_score(text_X, text_Y)

    pygame.display.update()
