import pygame

from src.utils.funcs import load_sound


class Player:
    def __init__(self, reload_time: float):
        self.reload_time = reload_time
        self.is_reloading = True
        self.current_reload_time = 0

        self.shot_sound = load_sound("sounds/game/shot.mp3")

    def update(self, delta_t):
        self.reload(delta_t)

    def reload(self, delta_t):
        if not self.is_reloading:
            self.current_reload_time += delta_t
            if self.current_reload_time >= self.reload_time:
                self.is_reloading = True
                self.current_reload_time = 0

    def shot(self):
        self.is_reloading = False
        self.current_reload_time = 0
        self.shot_sound.play()
