import pygame
import random
import math
from pygame import mixer

LENGTH = 600
BREADTH = 700
GameOver = False

# Screen Setup
pygame.init()
screen = pygame.display.set_mode((BREADTH, LENGTH))
pygame.display.set_caption("Covid Blaster")

# BackGround
icon = pygame.image.load("./spaceship.png")
pygame.display.set_icon(icon)
bg = pygame.image.load("./SafePlanet.jpg")

# Music
mixer.music.load("./SpaceMusic.mp3")
mixer.music.play(-1)

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyChangeX = []
EnemyChangeY = []
num_of_enemies = 8

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load("./alien.png"))
    EnemyX.append(random.randint(0, 636))
    EnemyY.append(random.randint(50, 150))
    EnemyChangeX.append(-3)
    EnemyChangeY.append(20)

# Player
PlayerImg = pygame.image.load("./spaceship.png")
PlayerX = 480
PlayerY = 510
PlayerChangeX = 0

# Bullet
BulletImg = pygame.image.load("./syringe1.png")
BulletX = 0
BulletY = 510
BulletChangeY = 0
BulletChangeY = 10
BulletFire = False

#   SCORE   
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
Ammo_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 32)
over_font1 = pygame.font.Font('freesansbold.ttf', 64)

def Show_score(x,y):
    score = font.render("Virus Remaining : " + str(num_of_enemies),True,(0,0,255))
    screen.blit(score,(x,y))
    # Ammo = font.render("Bullets Fired : " + str(Ammo_value),True,(50,205,50))
    # screen.blit(Ammo,(700,y))

def Game_Over(x,y):
    screen.blit(bg, (0, 0))
    over = over_font1.render("Congratratulations,",True,(0,0,0))
    screen.blit(over,(x,y))
    over2 = over_font.render("You Have Defeated COVID-19 ",True,(0,0,0))
    screen.blit(over2,(x,y+70))

def player(PlayerX, PlayerY):
    screen.blit(PlayerImg, (PlayerX, PlayerY))

def enemy(X, Y,i):
    screen.blit(EnemyImg[i], (X, Y))

def bullet(BulletX, BulletY):
    global BulletFire
    BulletFire = True
    screen.blit(BulletImg, (BulletX+16, BulletY+10))

def collision(X,Y,BulletX,BulletY):
    dis = math.sqrt(math.pow(X-BulletX,2)+math.pow(Y-BulletY,2))
    
    if dis <30:
        return True
    else:
        return False


while not GameOver:
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerChangeX = -5
            if event.key == pygame.K_RIGHT:
                PlayerChangeX = 5
            if event.key == pygame.K_SPACE:
                if not BulletFire:
                    # Ammo_value += 1
                    Bullet_sound = mixer.Sound("./laser.wav")
                    Bullet_sound.play()
                    BulletChangeY = -5
                    BulletX = PlayerX
                    bullet(BulletX,BulletY)
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerChangeX = 0


    # Player Motion
    PlayerX = PlayerX + PlayerChangeX
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 636:
        PlayerX = 636
    
    # Enemy Motion
    for i in range(num_of_enemies):

        if num_of_enemies == 0:
            Game_Over(0,0)
            break

        EnemyX[i] = EnemyX[i] + EnemyChangeX[i]
        if EnemyX[i] <= 0:
            EnemyChangeX[i] = 2
            EnemyY[i] += 20
        elif EnemyX[i] >= 636:
            EnemyChangeX[i] = -2
            EnemyY[i] += 20

    
    # screen.fill((0,0,0))
        col = collision(EnemyX[i],EnemyY[i],BulletX,BulletY)
        if col:
            Contact_sound = mixer.Sound("./explosion.wav")
            Contact_sound.play()        
            BulletY = 510
            BulletFire = False
            score_value +=1
            # print(score_value)
            num_of_enemies -=1
            # EnemyX[i] = random.randint(0, 936)
            # EnemyY[i] = random.randint(50, 150)
    
        enemy(EnemyX[i], EnemyY[i],i)
    
    if BulletY <= 0:
        BulletY = 510
        BulletFire =False
    if BulletFire:
        bullet(BulletX,BulletY)
        BulletY += BulletChangeY

    player(PlayerX, PlayerY)
    Show_score(textX,textY)
    if num_of_enemies == 0:
        Game_Over(0,0) 
    pygame.display.update()
