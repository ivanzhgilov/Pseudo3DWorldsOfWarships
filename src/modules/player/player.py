import math

import pygame

import src.consts
from src.modules.control_objects.control_targets_and_cannonballs import (
    ControlTargetsAndCannonballs,
)
from src.utils.funcs import load_image, load_sound

WIGHT, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT
MIN_HEIGHT_ANGLE, MAX_HEIGHT_ANGLE = (
    src.consts.MIN_HEIGHT_ANGLE,
    src.consts.MAX_HEIGHT_ANGLE,
)


class Player:
    def __init__(self, reload_time: float, obj: ControlTargetsAndCannonballs):
        self.reload_time = reload_time
        self.is_reloading = True
        self.current_reload_time = 0

        self.obj = obj

        self.gunsight = pygame.transform.smoothscale(
            load_image("images/game/gunsight.png"), (100, 100)
        )
        self.cannon = pygame.transform.smoothscale(
            load_image("images/game/cannon.png"), (680, 400)
        )

        self.shot_sound = load_sound("sounds/game/shot.mp3")
        self.angle_width = 0
        self.angle_height = 0
        self.mouse_sense = 0.05

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

    def shot(self):
        if self.is_reloading:
            self.is_reloading = False
            self.current_reload_time = 0
            self.shot_sound.play()
            self.obj.cannon_shot(self.angle_height, self.angle_width)
        else:
            pass

    def mouse_control(self, delta_t):
        if pygame.mouse.get_focused():
            x, y = pygame.mouse.get_pos()
            diff_wight, diff_height = WIGHT // 2 - x, HEIGHT // 2 - y

            angle_width = self.angle_width + diff_wight * delta_t * self.mouse_sense

            angle_height = self.angle_height + diff_height * delta_t * self.mouse_sense

            if angle_width < 0:
                angle_width += 2 * math.pi
            elif angle_width > 2 * math.pi:
                angle_width -= 2 * math.pi

            self.angle_width = angle_width

            self.angle_height = angle_height
            if angle_height > MAX_HEIGHT_ANGLE:
                self.angle_height = MAX_HEIGHT_ANGLE
            elif angle_height < MIN_HEIGHT_ANGLE:
                self.angle_height = MIN_HEIGHT_ANGLE
            else:
                self.angle_height = angle_height

    def draw(self, screen):
        screen.blit(
            self.gunsight, self.gunsight.get_rect(center=(WIGHT // 2, HEIGHT // 2))
        )
        screen.blit(
            self.cannon, self.cannon.get_rect(center=(WIGHT // 2, HEIGHT - 160))
        )
