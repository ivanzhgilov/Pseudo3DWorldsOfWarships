import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, a, b, z, *group):
        super().__init__(group)
        self._a = a
        self._b = b
        self._z = z


    def realize(self):
        pass
