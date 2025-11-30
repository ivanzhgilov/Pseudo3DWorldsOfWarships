import pygame

from src.utils.funcs import load_sound
from src.modules.control_objects.control_targets_and_cannonballs import ControlTargetsAndCannonballs

import src.consts

WIGHT, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


class Player:
    def __init__(self, reload_time: float):
        self.reload_time = reload_time
        self.is_reloading = True
        self.current_reload_time = 0

        self.shot_sound = load_sound("sounds/game/shot.mp3")
        self.angle_width = 0
        self.angle_height = 0
        self.mouse_sense = 0

    def update(self, delta_t):
        self.reload(delta_t)
        self.mouse_control(delta_t)

    def reload(self, delta_t):
        if not self.is_reloading:
            self.current_reload_time += delta_t
            if self.current_reload_time >= self.reload_time:
                self.is_reloading = True
                self.current_reload_time = 0

    def set_mouse_sense(self, mouse_sense):
        self.mouse_sense = mouse_sense

    def shot(self, obj: ControlTargetsAndCannonballs):
        if self.is_reloading:
            self.is_reloading = False
            self.current_reload_time = 0
            self.shot_sound.play()
            obj.cannon_shot(self.angle_height, self.angle_width)
        else:
            pass

    def mouse_control(self, delta_t):
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            diff_wight, diff_height = WIGHT // 2 - x, HEIGHT // 2 - y

            pygame.mouse.set_pos(WIGHT // 2, HEIGHT // 2)
            self.angle_width += diff_wight * delta_t * self.mouse_sense
            self.angle_height += diff_height * delta_t * self.mouse_sense

