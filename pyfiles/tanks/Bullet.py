import pygame

YELLOW = (255, 255, 0)
WIDTH, HEIGHT = 800, 600


class Bullet(pygame.sprite.Sprite):
    # direction constants

    (DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.direction = direction
        self.image = pygame.transform.scale(pygame.image.load('sprites/bullet/up.png'), (10, 20))
        self.rect = self.image.get_rect()
        if direction == self.DIR_UP:
            self.rect.x = x - 5
            self.rect.y = y - 20
            self.deltaY = -self.speed
        elif direction == self.DIR_RIGHT:
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect.x = x + 30
            self.rect.y = y + 15
            self.deltaX = self.speed
        elif direction == self.DIR_DOWN:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.x = x - 5
            self.rect.y = y + 40
            self.deltaY = self.speed
        elif direction == self.DIR_LEFT:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect.x = x - 30
            self.rect.y = y + 15
            self.deltaX = -self.speed

    def update(self):
        if self.direction == self.DIR_UP:
            self.rect.y += self.deltaY
        if self.direction == self.DIR_RIGHT:
            self.rect.x += self.deltaX
        if self.direction == self.DIR_DOWN:
            self.rect.y += self.deltaY
        if self.direction == self.DIR_LEFT:
            self.rect.x += self.deltaX
        # убить, если он заходит за  экран
        if self.rect.top < 0 or self.rect.bottom > HEIGHT or self.rect.right > WIDTH or self.rect.left < 0:
            self.kill()
