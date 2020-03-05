import pygame

from pyfiles.blocks.Brick import Brick
from pyfiles.blocks.Steel import Steel
from pyfiles.blocks.Bush import Bush
from pyfiles.blocks.Water import Water
from pyfiles.blocks.City import City
from pyfiles.blocks.Ice import Ice

bs = 50  # block size


class Field:
    def __init__(self, level_num):
        # группа разрушаемых блоков
        self.bricks = pygame.sprite.Group()
        # группа неразрушаемых
        self.unbreakable = pygame.sprite.Group()
        # группа для кустов
        self.plants = pygame.sprite.Group()
        # группа для воды
        self.water = pygame.sprite.Group()
        # группа для базы
        self.base = pygame.sprite.GroupSingle()
        level_path = 'levels/level_'+level_num+'.txt'
        self.level_path = level_path
        self.level = list()
        self.level_init()
        self.blocks_init()

    def level_init(self):
        # читаем уровень из файла и сохраняем его в level
        with open(self.level_path, 'r') as level_file:
            self.level = level_file.read().splitlines()

    def blocks_init(self):
        # состояние блока
        t, r, b, l = 'top', 'right', 'bottom', 'left'
        tl, tr, bl, br = 'top_left', 'top_right', 'bottom_left', 'bottom_right'

        y = 0
        for string in self.level:
            x = 0
            for char in string:
                if char != 'd':
                    # bricks addition
                    if char is '0':
                        self.bricks.add(Brick(x * bs, y * bs, r))
                    elif char is '1':
                        self.bricks.add(Brick(x * bs, y * bs, b))
                    elif char is '2':
                        self.bricks.add(Brick(x * bs, y * bs, l))
                    elif char in '3':
                        self.bricks.add(Brick(x * bs, y * bs, t))
                    elif char in '4':
                        # self.bricks.add(Brick(x * bs, y * bs)) # устаревший код
                        self.bricks.add(Brick(x * bs, y * bs, tl))
                        self.bricks.add(Brick(x * bs, y * bs, tr))
                        self.bricks.add(Brick(x * bs, y * bs, bl))
                        self.bricks.add(Brick(x * bs, y * bs, br))
                    elif char is 'o':
                        self.bricks.add(Brick(x * bs, y * bs, tl))
                    elif char is 'p':
                        self.bricks.add(Brick(x * bs, y * bs, tr))
                    elif char is 'q':
                        self.bricks.add(Brick(x * bs, y * bs, bl))
                    elif char is 'r':
                        self.bricks.add(Brick(x * bs, y * bs, br))
                    # unbreakable addition
                    elif char is '5':
                        self.unbreakable.add(Steel(x * bs, y * bs, r))
                    elif char is '6':
                        self.unbreakable.add(Steel(x * bs, y * bs, b))
                    elif char is '7':
                        self.unbreakable.add(Steel(x * bs, y * bs, l))
                    elif char is '8':
                        self.unbreakable.add(Steel(x * bs, y * bs, t))
                    elif char in '9':
                        self.unbreakable.add(Steel(x * bs, y * bs))
                    elif char is 'c':
                        self.unbreakable.add(Ice(x * bs, y * bs))
                    # other addition
                    elif char == 'b':
                        self.plants.add(Bush(x * bs, y * bs))
                    elif char == 'a':
                        self.water.add(Water(x * bs, y * bs))
                    elif char == 's':
                        self.base.add(City(x * bs, y * bs))
                x += 1
            y += 1

    def init_field_sprites_group(self):
        field_sprites = pygame.sprite.Group()
        for b in self.bricks:
            field_sprites.add(b)
        for b in self.unbreakable:
            field_sprites.add(b)
        for b in self.water:
            field_sprites.add(b)
        for b in self.base:
            field_sprites.add(b)
        return field_sprites
