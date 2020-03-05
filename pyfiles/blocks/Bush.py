import pygame
from pyfiles.blocks.Block import Block


class Bush(Block):
    def __init__(self, x, y, state='full'):
        super().__init__(x, y, state)
        # images
        self.standing = pygame.transform.scale(pygame.image.load('sprites/blocks/bushes/full.png'),
                                               (self.bs // 2, self.bs))
        self.lying = pygame.transform.scale(pygame.image.load('sprites/blocks/bushes/full.png'),
                                            (self.bs, self.bs // 2))
        self.full = pygame.transform.scale(pygame.image.load('sprites/blocks/bushes/full.png'),
                                           (self.bs, self.bs))
        self.quarter = pygame.transform.scale(pygame.image.load('sprites/blocks/bushes/full.png'),
                                              (self.bs // 2, self.bs // 2))
        self.set_image()
        self.update_rect()
