import pygame
import random
from pyfiles.tanks.Player1 import Player1
from pyfiles.battlefield.Field import Field
from pyfiles.menu.Game_over import Game_over
from pyfiles.tanks.Enemy import Enemy
from pyfiles.tanks.Player2 import Player2
from pyfiles.battlefield.Bonus import Bonus
from pyfiles.blocks.Brick import Brick

size = width, height = 800, 600
black = 0, 0, 0
white = 255, 255, 255


def game_over_screen(label, color):
    screen = Game_over(label, color)
    screen.show()
    return True


def merge_sprites_group(tanks, field):
    all_sprites = pygame.sprite.Group()
    for b in tanks:
        all_sprites.add(b)
    for b in field:
        all_sprites.add(b)
    return all_sprites


class GameLoop:
    def __init__(self):
        pass

    def one_player_loop(self, level_num, two=False):
        tanks_sprites = pygame.sprite.Group()  # объявляем группы спрайтов
        players_group = pygame.sprite.Group()
        bullets_of_players = pygame.sprite.Group()
        bullets_of_enemies = pygame.sprite.Group()

        bullets = list()

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 24, True)

        enemies_count = '10'
        player_lifes_count = '3'

        life_bonus = pygame.sprite.GroupSingle()
        grenade_bonus = pygame.sprite.GroupSingle()
        shovel_bonus = pygame.sprite.GroupSingle()

        pygame.init()
        screen = pygame.display.set_mode(size)  # инициализация pygame

        ui = pygame.sprite.Sprite()
        ui.image = pygame.image.load('sprites/ui.png')
        ui.rect = ui.image.get_rect()
        ui.rect.x = 650
        ui.rect.y = 0

        f = Field(level_num)  # инициализация поля, загрузка в field_sprites
        f.unbreakable.add(ui)
        field_sprites = f.init_field_sprites_group()  # группа спрайтов поля
        decorate = f.plants  # группа декоративных спрайтов

        tank_player = Player1(bullets_of_players, bullets)  # инициализация танка игрока
        players_group.add(tank_player)  # загрузка танка игрока

        if two:
            player2 = Player2(bullets_of_players, bullets)
            players_group.add(player2)

        pygame.font.init()  # Инициализация текста
        enemy1 = Enemy(bullets_of_enemies, bullets, 40, 40, players_group, '1')  # инициализация врагов

        tanks_sprites.add(enemy1)
        enemy_list = list()
        enemy_list.append(enemy1)

        ticks = 0
        enemies_count_flag = True

        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            for enemy in enemy_list:
                if not enemy.alive():
                    enemy_list.remove(enemy)

            if ticks >= 300:
                if len(enemy_list) < 4 and int(enemies_count) > 0 and int(enemies_count)-len(enemy_list) > 0:
                    new_enemy = Enemy(bullets_of_enemies, bullets, (random.randint(0, 12))*50 + 2, 40, players_group, str(random.randint(0, 3)))
                    while pygame.sprite.spritecollideany(new_enemy, tanks_sprites): # проверка, что враг не спавнится внутри другого
                        new_enemy = Enemy(bullets_of_enemies, bullets, (random.randint(0, 12))*50 + 2, 40, players_group, str(random.randint(0, 3)))
                    enemy_list.append(new_enemy)
                    tanks_sprites.add(new_enemy)
                    ticks = 0
                else:
                    ticks = 300
            # Обновление
            tanks_sprites.update()
            # field_sprites.update()
            players_group.update()
            bullets_of_players.update()
            bullets_of_enemies.update()

            screen.fill(black)

            # подготовка к отработке коллизий
            tanks_field = merge_sprites_group(tanks_sprites, field_sprites)
            player_field = merge_sprites_group(players_group, field_sprites)
            # коллизия танка
            for player in players_group:
                temp = merge_sprites_group(tanks_field, players_group)
                temp.remove(player)
                player.check_collisions(temp)
            for enemy in enemy_list:
                if enemy.alive():
                    temp = merge_sprites_group(tanks_field, player_field)
                    temp.remove(enemy)
                    enemy.check_collisions(temp)

            # отрисовка
            field_sprites.draw(screen)
            tanks_sprites.draw(screen)
            life_bonus.draw(screen)
            grenade_bonus.draw(screen)
            shovel_bonus.draw(screen)
            bullets_of_players.draw(screen)
            bullets_of_enemies.draw(screen)
            players_group.draw(screen)
            decorate.draw(screen)
            ts = font.render('Enemies: '+enemies_count, False, white)
            ts2 = font.render('Lifes: '+player_lifes_count, False, white)
            screen.blit(ts, (655, 500))
            screen.blit(ts2, (655, 400))

            for p in players_group:  # отработка бонусов
                if pygame.sprite.spritecollide(p, life_bonus, True):
                    player_lifes_count = str(int(player_lifes_count) + 1)
                if pygame.sprite.spritecollide(p, grenade_bonus, True):
                    for e in enemy_list:
                        if e.isAlive:
                            e.kill()
                            enemies_count = str(int(enemies_count) - 1)
                    if (int(enemies_count)) <= 0:
                        enemies_count_flag = False
                        game_over = game_over_screen('You won!', 'green')
                        return 'win'
                if pygame.sprite.spritecollide(p, shovel_bonus, True):
                    tl, tr, bl, br = 'top_left', 'top_right', 'bottom_left', 'bottom_right'
                    f.bricks.add(Brick(5 * 50, 11 * 50, br))
                    f.bricks.add(Brick(5 * 50, 11 * 50, tr))
                    f.bricks.add(Brick(5 * 50, 10 * 50, br))
                    f.bricks.add(Brick(6 * 50, 10 * 50, br))
                    f.bricks.add(Brick(6 * 50, 10 * 50, bl))
                    f.bricks.add(Brick(7 * 50, 11 * 50, bl))
                    f.bricks.add(Brick(7 * 50, 11 * 50, tl))
                    f.bricks.add(Brick(7 * 50, 10 * 50, bl))

            # коллизия снарядов с полем
            if len(bullets) > 0:
                for b in bullets:  # удалить "мёртвые" снаряды (оптимизация)
                    if not b.alive():
                        bullets.remove(b)

                for b in bullets:  # коллизия снарядов и блоков
                    if pygame.sprite.spritecollideany(b, f.bricks) or pygame.sprite.spritecollideany(b, f.unbreakable):
                        collided = pygame.sprite.spritecollide(b, f.bricks, True)  # уничтожить блок
                        # for i in collided:                         # это старый функционал разрушаемости блоков.
                        # i.take_damage(b.direction)
                        field_sprites = f.init_field_sprites_group()  # изменить поле
                        b.kill()

                for b in bullets:  # коллизия снарядов и базы
                    if pygame.sprite.spritecollideany(b, f.base):
                        pygame.sprite.spritecollide(b, f.base, 1)
                        game_over = game_over_screen('Game over', 'red')
                        return 'lose'

                for b in bullets:  # коллизия снарядов и танка игрока
                    if pygame.sprite.spritecollideany(b, players_group):
                        collided = pygame.sprite.spritecollide(b, players_group, False)
                        player_lifes_count = str(int(player_lifes_count) - 1)
                        if int(player_lifes_count) <= 0:
                            game_over = game_over_screen('Game over', 'red')
                            return 'lose'
                        else:
                            for i in collided:
                                i.respawn()
                            for tank in tanks_sprites:
                                tank.player = players_group
                        if int(player_lifes_count) is not 3 and len(life_bonus) == 0 and random.randint(0, 1) == 0:
                            life = Bonus(random.randint(1, 11) * 50 + 2, random.randint(1, 11) * 50 + 2, 'life')
                            life_bonus.add(life)
                        b.kill()

                for b in bullets_of_players:  # коллизия снаряда и противника
                    if pygame.sprite.spritecollide(b, tanks_sprites, True):
                        if enemies_count_flag:
                            enemies_count = str(int(enemies_count) - 1)
                        if (int(enemies_count)) <= 0:
                            enemies_count_flag = False
                            game_over = game_over_screen('You won!', 'green')
                            return 'win'
                        b.kill()
                        if int(enemies_count) > 0:
                            for enemy in enemy_list:
                                if not enemy.isAlive:
                                    new_enemy = Enemy(bullets_of_enemies, bullets, (random.randint(0, 12)) * 50 + 2, 40, players_group, str(random.randint(0, 3)))
                                    while pygame.sprite.spritecollideany(new_enemy, tanks_sprites) or pygame.sprite.spritecollideany(new_enemy, players_group):  # проверка, что враг не спавнится внутри другого
                                        new_enemy = Enemy(bullets_of_enemies, bullets, (random.randint(0, 12)) * 50 + 2, 40,players_group, str(random.randint(0, 3)))
                                    enemy = new_enemy
                                    tanks_sprites.add(enemy)
                        if random.randint(0, 10) == 0:
                            grenade = Bonus(random.randint(1, 11) * 50 + 2, random.randint(1, 11) * 50 + 2, 'grenade')
                            grenade_bonus.add(grenade)
                        if random.randint(0, 10) == 1:
                            shovel = Bonus(random.randint(1, 11) * 50 + 2, random.randint(1, 11) * 50 + 2, 'shovel')
                            shovel_bonus.add(shovel)

                pygame.sprite.groupcollide(bullets_of_enemies, bullets_of_players, True, True)  # коллизия снарядов

            pygame.display.flip()
            pygame.time.wait(10)
            ticks += 1
