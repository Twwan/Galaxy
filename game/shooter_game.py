from pygame import *
from random import randint
font.init()
'''Необходимые классы'''

class GameSprite(sprite.Sprite):    #конструктор класса
    def __init__(self, in_image, in_size_x, in_size_y, in_coord_x, in_coord_y):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(in_image), (in_size_x, in_size_y))
        self.rect = self.image.get_rect()
        self.rect.x = in_coord_x
        self.rect.y = in_coord_y
        self.size_x = in_size_x
        self.size_y = in_size_y
    def blit(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class MoveSprite(GameSprite):    #конструктор класса
    def __init__(self, in_image, in_size_x, in_size_y, in_coord_x, in_coord_y, in_speed):
        super().__init__(in_image, in_size_x, in_size_y, in_coord_x, in_coord_y)
        self.speed = in_speed
    def move(self,x,y):
        self.rect.x += self.speed*x
        self.rect.y += self.speed*y

class PlayerSprite(MoveSprite):
    def move(self):       
       keys = key.get_pressed()
       if keys[K_a] and self.rect.x > self.speed:
           super().move(-1,0)
       if keys[K_d] and self.rect.x < win_width - self.size_x:
           super().move(1,0)
    def fire(self):
        bullets.add(BulletSprite('bullet.png', 30, 30, self.rect.centerx-30/2,self.rect.top,5))

class EnemySprite(MoveSprite):
    def move(self):
       if self.rect.y >= win_width:
           bots.lost += 1
           self.rect.y = -50
           self.rect.x = randint(20, win_width - 50)
           self.speed = randint(2,4)       
       super().move(0,1)
    def update(self):
        self.move()
        self.blit()
    def kill(self):
        bots.kills += 1
        self.rect.y = -50
        self.rect.x = randint(1, win_width-10)
        self.speed = randint(1, 3)
        self.update()
        
class AsteroidSprite(MoveSprite):
    def move(self):
       if self.rect.y >= win_width:
           self.rect.y = randint(-5000, -3000)
           self.rect.x = randint(20, win_width - 50)
           self.speed = randint(2, 3)       
       super().move(0,1)
    def update(self):
        self.move()
        self.blit()

class BulletSprite(MoveSprite):
    def move(self):
       if self.rect.y <= 0:
           bullets.remove(self)
       super().move(0,-1)
    def update(self):
        self.move()
        self.blit()

#Игровая сцена:
win_width = 700
win_height = 500
sprite_size = 50
sprite_size1 = 70
window = display.set_mode((win_width, win_height))
display.set_caption("Космос")
background = GameSprite('galaxy.jpg', win_width,win_height,0,0)

#Персонажи игры:
bots = sprite.Group()
for i in range(5):
    bots.add(EnemySprite('ufo.png', sprite_size1,sprite_size,randint(20, win_width - 50), -50 ,randint(1, 3)))

asteroid = sprite.Group()
for i in range(2):
    asteroid.add(AsteroidSprite('ast.png', randint(40, 80),randint(40, 80),randint(20, win_width - 50), randint(-50, 0) ,randint(2,3)))

player = PlayerSprite('rocket.png', sprite_size,sprite_size1,340,420,5)

bullets = sprite.Group()
puli = 10
#
game = True
clock = time.Clock()
FPS = 60

#счётчик
bots.lost = 0
bots.kills = 0
health = 3
font = font.SysFont('Arial', 20)

win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))
#музыка
#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
finish = False
cooldown = False
time = 0
count = 5/FPS
while game:
    keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                puli -= 1
                player.fire()
    
    background.blit()
    if cooldown == True:
            if time < count:
                time += 1
            else:
                puli = 10
                cooldown == False
    if finish != True:
        player.blit()
        player.move()
        bots.update()
        asteroid.update()
        if puli == 0:
            cooldown = True
        if health == 0:
            finish = True
            result = lose
        if sprite.spritecollide(player,bots,True):
            health -= 1
        if sprite.spritecollide(player,asteroid,False):
            finish = True
            result = lose
        if bots.kills == 50:
            finish = True
            result = win
        if bots.lost == 20:
            finish = True
            result = lose
        lost_text = font.render('Пропущено: ' + str(bots.lost), 1, (255, 255, 255))
        bullets.update()

        bots_kill = sprite.groupcollide(bullets, bots, True, True)

        for bot in bots_kill:
            bot.kill()

        
        kill_text = font.render('Убито: ' + str(bots.kills), 1, (255, 255, 255))
        health_text = font.render('Жизней: ' + str(health), 1, (255, 255, 255))
        window.blit(kill_text, (10,10))
        window.blit(lost_text, (10,30))
        window.blit(health_text, (10,50))
    else:
        window.blit(result, (300, 200))
    
    display.update()
    clock.tick(FPS)