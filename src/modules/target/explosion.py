import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(group)

    def realize(self):
        pass