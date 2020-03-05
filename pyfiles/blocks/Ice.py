import pygame
from pyfiles.blocks.Block import Block


class Ice(Block):
    def __init__(self, x, y, state='full'):
        super().__init__(x, y, state)
        # images
        self.full = pygame.transform.scale(pygame.image.load('sprites/blocks/ice/full.png'),
                                           (self.bs, self.bs))
        self.set_image()
        self.update_rect()
