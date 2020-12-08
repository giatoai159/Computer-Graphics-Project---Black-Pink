import pygame
from Game import Game


def main():
    game = Game("Test")
    game.loop()


if __name__ == '__main__':
    main()

pygame.quit()
