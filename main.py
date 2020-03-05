from pyfiles.menu.MainMenu import MainMenu
from pyfiles.GameLoop import GameLoop


def main():
    level = '1'
    game = GameLoop()
    while True:
        menu = MainMenu()
        cmd = menu.show()

        flag = ''

        if cmd == 1:
            flag = game.one_player_loop(level)

        if cmd == 2:
            flag = game.one_player_loop(level, True)

        if flag == 'win':
            level = str(int(level) + 1)
        if int(level) is 4:
            level = '1'


if __name__ == '__main__':
    main()
