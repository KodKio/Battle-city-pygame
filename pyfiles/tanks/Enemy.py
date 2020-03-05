import pygame
import random
from pyfiles.tanks.Tank import Tank
from pyfiles.tanks.Bullet import Bullet

WIDTH, HEIGHT = 800, 600
block_size = 40


class Enemy(Tank):
    def __init__(self, sprites, bullets, x, y, player, mode):
        pic_u = pygame.transform.scale(pygame.image.load('sprites/enemy1/enemy_u.png'), (block_size, block_size))
        pic_r = pygame.transform.scale(pygame.image.load('sprites/enemy1/enemy_r.png'), (block_size, block_size))
        pic_d = pygame.transform.scale(pygame.image.load('sprites/enemy1/enemy_d.png'), (block_size, block_size))
        pic_l = pygame.transform.scale(pygame.image.load('sprites/enemy1/enemy_l.png'), (block_size, block_size))
        super().__init__(sprites, bullets, pic_u, pic_l, pic_d, pic_r)
        self.rect.centerx = x
        self.rect.bottom = y
        self.distance = 0
        self.cmd_choice = 0
        self.bullet = Bullet(0,0,0)
        self.bullet.kill()
        self.player = player
        self.direction_glitch = False
        self.mode = mode
        self.glitch_set = list()
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def shoot(self):
        if not self.bullet.alive() and self.shooting_cooldown == 0:
            self.bullet = Bullet(self.rect.centerx, self.rect.top, self.direction)
            self.sprites.add(self.bullet)
            self.shooting_cooldown = 50
            self.bullets.append(self.bullet)

    def update(self):
        super().update()
        self.deltaX = 0
        self.deltaY = 0
        self.choose_cmd()
        # выбирает стрелять или нет. Шанс 1 к 11
        now = pygame.time.get_ticks()
        if self.mode is not '3':
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot()
        self.move()
        self.check_collisions()
        self.set_sprite_picture()
        self.glitch_analyze()

    def move(self):
        if self.is_able_to_move is False:
            self.distance = 0
        self.choose_direction()
        if self.direction is 0:
            self.distance -= self.speed
            self.move_up()
        elif self.direction is 1:
            self.distance -= self.speed
            self.move_right()
        elif self.direction is 2:
            self.distance -= self.speed
            self.move_down()
        elif self.direction is 3:
            self.distance -= self.speed
            self.move_left()

    def choose_direction(self):
        if self.distance <= 0 and not self.direction_glitch:
            self.direction = random.randint(0, 3)
            self.distance = 50 * random.randint(1, 2)
        if self.direction_glitch:
            self.direction_glitch = False

    # def respawn(self):
    # self.__init__(self.sprites, self.bullets, self.rect.x, self.rect.y, self.player, self.mode)

    def glitch_analyze(self):
        a = (self.rect.x, self.rect.y)
        self.glitch_set.append(a)

        if len(self.glitch_set) > 40:
            if check_equal3(self.glitch_set):
                # print('ANTI GLITCH MOVE')
                self.move()
                self.check_collisions()
            self.glitch_set = list()

    def choose_cmd(self):
        # if self.distance <= 0:
        # print('Enemy', self.rect.x, self.rect.y)
        for p in self.player:
            if self.mode == '3':
                if numbers_close(p.rect.y, self.rect.y):
                    if p.rect.x > self.rect.x:
                        self.direction = 1
                    else:
                        self.direction = 3
                    self.shoot()
                    self.direction_glitch = True
                elif numbers_close(p.rect.x, self.rect.x):
                    if p.rect.y > self.rect.y:
                        self.direction = 2
                    else:
                        self.direction = 0
                    self.shoot()
                    self.direction_glitch = True
            if self.mode == '2':
                choice = random.randint(0, 5)
                if choice <= 4:
                    if numbers_close(p.rect.y, self.rect.y):
                        if p.rect.x > self.rect.x:
                            self.direction = 1
                        else:
                            self.direction = 3
                        self.shoot()
                        self.direction_glitch = True
                    elif numbers_close(p.rect.x, self.rect.x):
                        if p.rect.y > self.rect.y:
                            self.direction = 2
                        else:
                            self.direction = 0
                        self.shoot()
                        self.direction_glitch = True

            if self.mode == '1':
                if numbers_close(p.rect.y, self.rect.y):
                    if p.rect.x > self.rect.x and self.direction == 1:
                        self.shoot()
                    elif p.rect.x < self.rect.x and self.direction == 3:
                        self.shoot()
                    self.direction_glitch = True
                elif numbers_close(p.rect.x, self.rect.x):
                    if p.rect.y > self.rect.y and self.direction == 2:
                        self.shoot()
                    elif p.rect.y < self.rect.y and self.direction == 0:
                        self.shoot()
                    self.direction_glitch = True


def numbers_close(a, b):
    if abs(a-b) < 6:
        return True
    else:
        return False


def check_equal3(lst):
    return lst[1:] == lst[:-1]

