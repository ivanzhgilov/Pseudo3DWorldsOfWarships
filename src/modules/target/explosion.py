import random

import pygame

from src.utils.funcs import load_sound


class Explosion(pygame.sprite.Sprite):
    def __init__(self, a, b, z, *group):
        super().__init__(group)
        self._a = a
        self._b = b
        self._z = z

        path = "sounds/game/hit_sounds/"
        sound_1 = load_sound(path + "ahah.mp3")
        sound_2 = load_sound(path + "bombaaa.mp3")
        sound_3 = load_sound(path + "naa.mp3")
        sound_4 = load_sound(path + "hyhy.mp3")
        sound_5 = load_sound(path + "nya.mp3")
        sound_5.set_volume(0.5)
        sound_6 = load_sound(path + "uaua.mp3")

        self.sounds = [sound_1, sound_2, sound_3, sound_4, sound_5, sound_6]


    def realize(self):
        sound = random.choice(self.sounds)
        sound.play()
