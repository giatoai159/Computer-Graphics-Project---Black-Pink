from packages import *
from Game import *

def main():
    game = Game("Test")
    game.start()
    game.loop()


if __name__ == '__main__':
    main()

pygame.quit()
