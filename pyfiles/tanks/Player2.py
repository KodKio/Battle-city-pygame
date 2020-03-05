import pygame
from pyfiles.tanks.Tank import Tank
from pyfiles.tanks.Bullet import Bullet

block_size = 40

WIDTH, HEIGHT = 800, 600


class Player2(Tank):
    def __init__(self, sprites, bullets):
        pic_u = pygame.transform.scale(pygame.image.load('sprites/tank/tank_u.png'), (block_size, block_size))
        pic_r = pygame.transform.scale(pygame.image.load('sprites/tank/tank_r.png'), (block_size, block_size))
        pic_d = pygame.transform.scale(pygame.image.load('sprites/tank/tank_d.png'), (block_size, block_size))
        pic_l = pygame.transform.scale(pygame.image.load('sprites/tank/tank_l.png'), (block_size, block_size))
        super().__init__(sprites, bullets, pic_u, pic_l, pic_d, pic_r)
        self.bullet = Bullet(0,0,0)
        self.rect.centerx = WIDTH / 2 - 155
        self.bullet.kill()

    def shoot(self):
        if not self.bullet.alive() and self.shooting_cooldown == 0:
            self.bullet = Bullet(self.rect.centerx, self.rect.top, self.direction)
            self.sprites.add(self.bullet)
            self.shooting_cooldown = 15
            self.bullets.append(self.bullet)

    def update(self):
        super().update()
        self.deltaX = 0
        self.deltaY = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.move_left()
        elif keystate[pygame.K_RIGHT]:
            self.move_right()
        elif keystate[pygame.K_UP]:
            self.move_up()
        elif keystate[pygame.K_DOWN]:
            self.move_down()
        if keystate[pygame.K_RETURN]:
            self.shoot()
        self.check_collisions()
        self.set_sprite_picture()
        # print('Player', self.rect.x, self.rect.y)

    def useless(self):
        pass

    def respawn(self):
        self.__init__(self.sprites, self.bullets)
