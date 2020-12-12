import pygame
from Game import Game


def main():
    game = Game("Flappy Bird")
    game.loop()


if __name__ == '__main__':
    main()

pygame.quit()
