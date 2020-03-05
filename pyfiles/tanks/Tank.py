import pygame
from pyfiles.tanks.Bullet import Bullet

GREEN = (0, 255, 0)
WIDTH, HEIGHT = 800, 600


class Tank(pygame.sprite.Sprite):
    def __init__(self, sprites_group, bullets, pic_u, pic_l, pic_d, pic_r):
        pygame.sprite.Sprite.__init__(self)
        self.isAlive = True
#       self.hp = 1
        self.speed = 2
        self.direction = 0
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.deltaX = 0
        self.deltaY = 0
        self.bullets = bullets
        self.sprites = sprites_group
        self.backupXY = self.rect.x, self.rect.y
        self.is_able_to_move = True
        self.shooting_cooldown = 0
        self.pic_u = pic_u
        self.pic_r = pic_r
        self.pic_d = pic_d
        self.pic_l = pic_l

    def update(self):
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1

    def move_left(self):
        self.deltaX = -self.speed
        self.direction = 3

    def move_right(self):
        self.deltaX = self.speed
        self.direction = 1

    def move_up(self):
        self.deltaY = -self.speed
        self.direction = 0

    def move_down(self):
        self.deltaY = self.speed
        self.direction = 2

    def check_collisions(self, field_sprites=None):
        if field_sprites is not None:
            if pygame.sprite.spritecollideany(self, field_sprites):
                self.is_able_to_move = False
                self.rect.x, self.rect.y = self.backupXY
        else:
            if self.is_able_to_move:
                self.backupXY = self.rect.x, self.rect.y
                self.rect.x += self.deltaX
                self.rect.y += self.deltaY
            else:
                self.is_able_to_move = True
                self.rect.x, self.rect.y = self.backupXY

            # строки self.is_able_to_move = False в каждом if нужны, чтобы враг не упирался в стену
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.is_able_to_move = False
            if self.rect.left < 0:
                self.rect.left = 0
                # self.is_able_to_move = False
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.is_able_to_move = False
            if self.rect.top < 0:
                self.rect.top = 0
                # self.is_able_to_move = False

    def set_sprite_picture(self):
        if self.direction is 0:
            self.image = self.pic_u
        elif self.direction is 1:
            self.image = self.pic_r
        elif self.direction is 2:
            self.image = self.pic_d
        else:
            self.image = self.pic_l


