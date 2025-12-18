import pygame

from src import consts
from src.modules.game import Game, start_game

pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((consts.WIDTH, consts.HEIGHT))


def main():
    while True:
        start_game(screen)
        game = Game(screen)
        game.setup()
        game.start()


if __name__ == "__main__":
    main()
