import pygame
import sys


class Game_over:
    def __init__(self, label, color):
        self.size = 800, 600
        self.colors = {"red": (255, 0, 0),
                       "green": (0, 255, 0),
                       "blue": (0, 0, 255),
                       "white": (255, 255, 255),
                       "black": (0, 0, 0),
                       "brown": (153, 76, 0),
                       "grey": (100, 100, 100)}
        self.screen = pygame.display.set_mode(self.size)
        self.data0 = label
        self.color = self.colors[color]

    def show(self):
        pygame.init()
        pygame.font.init()

        screen = pygame.display.set_mode(self.size)

        font = pygame.font.SysFont('Comic Sans MS', 145, True)

        # self.data0 = 'Game over'
        # --------------
        game_over = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            screen.fill(self.colors["black"])

            ts0 = font.render(self.data0, False, self.color)  # главный текст пробития
            screen.blit(ts0, (70, 200))

            pygame.display.flip()
            pygame.time.wait(1000)
            game_over = True


def main():
    game_over = Game_over()
    game_over.show()


if __name__ == '__main__':
    main()
