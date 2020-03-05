import pygame
from pyfiles.blocks.Block import Block


class Brick(Block):

    def __init__(self, x, y, state='full'):
        super().__init__(x, y, state)
        # images
        self.standing = pygame.transform.scale(pygame.image.load('sprites/blocks/bricks/standing.png'),
                                               (self.bs // 2, self.bs))
        self.lying = pygame.transform.scale(pygame.image.load('sprites/blocks/bricks/lying.png'),
                                            (self.bs, self.bs // 2))
        self.full = pygame.transform.scale(pygame.image.load('sprites/blocks/bricks/full.png'),
                                           (self.bs, self.bs))
        self.quarter = pygame.transform.scale(pygame.image.load('sprites/blocks/bricks/quarter3.png'),
                                              (self.bs // 2, self.bs // 2))
        self.set_image()
        self.update_rect()

    def take_damage(self, bullet_direction):
        self.hp -= 1
        # если снаряд попадает в половинку блока со стороны большей по размеру, то он уничтожается
        if (bullet_direction == 0 or bullet_direction == 2) and (
                self.state == self.t or self.state == self.b) or (
                bullet_direction == 1 or bullet_direction == 3) and (
                self.state == self.l or self.state == self.r):
            self.hp = 0

        if self.hp == 0:
            print('brick was destroyed')
            self.kill()
            return
        elif self.hp == 1:
            print('brick was damaged to quarter')
            self.set_quarter_state(bullet_direction)
        elif self.hp == 2:
            print('brick was damaged to half')
            self.set_half_state(bullet_direction)
        self.set_image()
        self.correct_cords()
        self.update_rect()

    def set_half_state(self, bullet_direction=0):
        if bullet_direction == 0:
            self.state = self.t
        elif bullet_direction == 1:
            self.state = self.r
        elif bullet_direction == 2:
            self.state = self.b
        elif bullet_direction == 3:
            self.state = self.l

    def set_quarter_state(self, bullet_direction):
        if (bullet_direction == 1) and (self.state == self.t):
            self.state = self.tr
        elif bullet_direction == 1 and self.state == self.b:
            self.state = self.br
        elif bullet_direction == 3 and self.state == self.t:
            self.state = self.tl
        elif bullet_direction == 3 and self.state == self.b:
            self.state = self.bl
        elif bullet_direction == 2 and self.state == self.l:
            self.state = self.bl
        elif bullet_direction == 2 and self.state == self.r:
            self.state = self.br
        elif bullet_direction == 0 and self.state == self.l:
            self.state = self.tl
        elif bullet_direction == 0 and self.state == self.r:
            self.state = self.tr
