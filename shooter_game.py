from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (0, 255, 0))
lose = font1.render('GAME OVER', True, (255, 0, 0))
font2 = font.Font(None, 36)
score = 0
lost = 0 
# МАКС пропущено
max_lost = 10  
# Жизни игрока
life = 3
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 5:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 20, -10)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width -80)
            self.rect.y = -40
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width -80)
            self.rect.y = -40

win_width = 700
win_height = 500
player = Player('rocket.png', 5, win_height - 105, 80, 100, 10)
window = display.set_mode((win_width, win_height), FULLSCREEN)
display.set_caption('Оса')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 40, randint(1,5))
    monsters.add(monster)
for i in range(2):
    asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -40, 100, 100, randint(1,7))
    asteroids.add(asteroid)

rel_time = False
num_fire = 0

game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            
    if not finish:
        window.blit(background, (0, 0))

        text_score = font2.render('Счёт:' + str(score), True, (255, 0, 0))
        window.blit(text_score, (10, 20))
        text_lost = font2.render('Пропущенно:' + str(lost), True, (255, 0, 0))
        window.blit(text_lost, (10, 50))
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 40, randint(1, 5))
            monsters.add(monster)

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()
        
        if sprite.spritecollide(player, monsters, True):
            life -= 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 40, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(player, asteroids, True):
            asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -40, 100, 100, randint(1,7))
            asteroids.add(asteroid)
            life -= 1

        if life == 3:
            life_color = (0, 255, 0)
        if life == 2:
            life_color = (0, 250, 250)
        if life == 1:
            life_color = (200, 0, 0)
        if life == 0:
            life_color = (255, 0, 0)

        text_life = font1.render(str(life), True, life_color)
        window.blit(text_life, (650, 10))
        
        bullets.draw(window)
        bullets.update()
        
        if rel_time == True:
            now = timer()

            if now - last_time < 3:
                reload = font2.render('Wait, reload...', True, (255, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        display.update()
        #clock.tick(FPS)

        if lost >= max_lost or life == 0:
            window.blit(lose, (200, win_height // 2))
            display.flip()
            finish = True

        if score == 20:
            window.blit(win, (200, win_height // 2))
            display.flip()
            finish = True

    time.delay(50)