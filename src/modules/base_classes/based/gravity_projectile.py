import math

import pygame
import src.consts

GRAVITY_POWER = src.consts.GRAVITY_POWER
"""
Класс для снарядов с гравитацией, в дочерних классах в update() используем super() или ручками добавляем метод flight()
"""


class GravityProjectile(pygame.sprite.Sprite):
    def __init__(self, start_speed, angle_height, angle_width, *group, x=0, y=0, z=0):
        super().__init__(group)
        self.cord_z = z
        self.cord_x = x
        self.cord_y = y
        self.speed = start_speed
        self.angle_height = angle_height
        self.angle_width = angle_width
        self.speed_z = start_speed * math.sin(angle_height)
        self.speed_x = start_speed * math.cos(angle_height) * math.cos(angle_width)
        self.speed_y = start_speed * math.cos(angle_height) * math.sin(angle_width)

    def update(self, delta_t):
        self.flight(delta_t)

    def move(self, delta_t):
        self.cord_z += self.speed_z * delta_t
        self.cord_y += self.speed_y * delta_t
        self.cord_x += self.speed_x * delta_t

    def gravity(self, delta_t):
        self.speed_z -= GRAVITY_POWER * delta_t

    def is_fall(self):
        if self.cord_z <= 0:
            return True
        return False

    def delete_projectile(self):
        self.kill()

    def flight(self, delta_t):
        self.move(delta_t)
        self.gravity(delta_t)
        if self.is_fall():
            self.delete_projectile()
