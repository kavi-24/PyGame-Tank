import random

import pygame
pygame.init()
pygame.font.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((220, 220, 220))
pygame.mouse.set_visible(False)
pygame.display.set_caption("JUST ANOTHER GAME")

enemies = []


class Laser:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 15
        self.height = 5

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))


class Player:
    def __init__(self, img, x, y, life=100):
        self.img = img
        self.x = x
        self.y = y
        self.life = life
        self.width = img.get_width()
        self.height = img.get_height()
        self.yVel = 0.8
        self.lasers = []

    def moveUp(self):
        self.y -= self.yVel
        if self.y < 20:
            self.y = 20

    def moveDown(self):
        self.y += self.yVel
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

    def drawHealth(self):
        pygame.draw.rect(screen, (0, 0, 255),
                         (self.x, self.y-20, self.img.get_width(), 15), 3)
        pygame.draw.rect(screen, (255, 0, 0), (self.x+2, self.y-18,
                         (self.img.get_width() * (self.life/100))-3, 11))

    def makeLaser(self):
        if len(self.lasers) < 5:
            self.lasers.append(
                Laser(self.x + self.width, self.y + self.height/2 - 5, (0, 255, 0)))

    def moveLaser(self):
        for laser in self.lasers:
            laser.x += 0.5
            if laser.x > WIDTH:
                self.lasers.remove(laser)
            laser.draw()

    def draw(self):
        screen.blit(self.img, (self.x, self.y))
        self.drawHealth()
        self.moveLaser()


class Enemy:
    def __init__(self, img, x, y):
        self.img = img
        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.xVel = 0.2
        self.lasers = []
        if len(self.lasers) < 2:
            enemies.append(self)

    def makeLaser(self):
        if pygame.time.get_ticks() % random.randint(100, 1000) == 0:
            if len(self.lasers) < 4:
                self.lasers.append(
                    Laser(self.x - self.width + 5, self.y + self.height/2 - 5, (0, 255, 255)))

    def moveLaser(self):
        for laser in self.lasers:
            laser.x -= 0.3
            if laser.x < 0:
                self.lasers.remove(laser)
            laser.draw()

    def draw(self):
        self.x -= self.xVel
        if self.x < 0:
            enemies.remove(self)
        screen.blit(self.img, (self.x, self.y))
        self.moveLaser()

def scoreCount():
    global score

    font = pygame.font.SysFont("comicsansms", 72)
    text = font.render(f"Score: {score}", True, (192, 192, 192))
    screen.blit(text, (WIDTH/2 - text.get_width() /
                2, HEIGHT/2 - text.get_height()/2))

def gameOver():
    global score

    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((220, 220, 220))

        font = pygame.font.SysFont("comicsansms", 72)

        
        text = font.render(f"GAME OVER", True, (150, 150, 150))
        screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2-100))
        
        text = font.render(f"YOUR SCORE WAS {score}", True, (150, 150, 150))
        screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
        
        text = font.render(f"PRESS ANY KEY TO QUIT", True, (150, 150, 150))
        screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2+100))
    
        pygame.display.update()

try:
    player = Player(pygame.image.load("player.png"), 20, 20, 100)
except:
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    player = Player(pygame.image.load("player.png"), 20, 20, 100)
score = 0
run = True
paused = False

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameOver()
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_SPACE and not paused:
                player.makeLaser()

    if not paused:

        if pygame.time.get_ticks() % 1500 == 0:
            Enemy(pygame.image.load("enemy.png"), random.randint(
                WIDTH, WIDTH+600), random.randint(40, HEIGHT-40))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.moveUp()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.moveDown()

        for enemy in enemies:
            for laser in player.lasers:
                if laser.x > enemy.x and laser.x < enemy.x + enemy.width and laser.y > enemy.y and laser.y < enemy.y + enemy.height:
                    player.lasers.remove(laser)
                    enemies.remove(enemy)
                    score += 1

            for laser in enemy.lasers:
                if laser.x <= player.x + player.width and player.y < laser.y < player.y + player.height:
                    enemy.lasers.remove(laser)
                    player.life -= 10
                    if player.life <= 0:
                        gameOver()

            if enemy.x > player.x and enemy.x < player.x + player.width and enemy.y > player.y and enemy.y < player.y + player.height:
                player.life -= 10
                enemies.remove(enemy)
                score -= 1
                if player.life <= 0:
                    gameOver()

        screen.fill((220, 220, 220))

        scoreCount()
        for enemy in enemies:
            enemy.draw()
            enemy.makeLaser()
        player.draw()
    else:
        screen.fill((220, 220, 220))
        font = pygame.font.SysFont("comicsansms", 72)
        text = font.render("PAUSED", True, (192, 192, 192))
        screen.blit(text, (WIDTH/2 - text.get_width() /
                           2, HEIGHT/2 - text.get_height()/2))

    pygame.display.update()
