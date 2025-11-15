import pygame

import src.consts
from src.modules.target.explosion import Explosion
import random

MAP_SIZE = src.consts.MAP_SIZE
CELL_SIZE = src.consts.CELL_SIZE
RESERVED_CELLS = src.consts.RESERVED_CELLS
MIN_Z, MAX_Z = src.consts.MIN_Z, src.consts.MAX_Z
MAX_PERSENT_FIELD_OCCUPANCY = src.consts.MAX_PERSENT_FIELD_OCCUPANCY


class Target(pygame.sprite.Sprite):
    def __init__(self, img, a, b, z, explosion_group: pygame.sprite.Group, *group, height_object=CELL_SIZE // 2):
        """
        a, b - положение клетки
        z - координата центра по высоте
        height_object - половина высоты цели
        """
        super().__init__(group)
        self.image = img
        self.a = a
        self.b = b
        self.z_min = z - height_object
        self.z_max = z + height_object
        self.explosion_group = explosion_group

    def destroy(self):
        self.kill()
        explosion = Explosion(self.explosion_group)
        explosion.realize()

    def collide_cell(self, a, b):
        if a == self.a and b == self.b:
            return True
        return False

    def collide_height(self, z):
        if self.z_min <= z <= self.z_max:
            return True
        return False

    def collide(self, a, b, z):
        if self.collide_cell(a, b) and self.collide_height(z):
            return True
        return False

    def get_coords(self):
        return self.a, self.b


class ListTarget:
    def __init__(self, spawn_time, img_target, target_group: pygame.sprite.Group, explosion_group: pygame.sprite.Group):
        # noinspection PyCompatibility
        self.list: list[Target] = []
        # noinspection PyCompatibility
        self.used_coords: list[tuple[int, int]] = RESERVED_CELLS
        self.target_group = target_group
        self.explosion_group = explosion_group
        self.image_target = img_target
        self.spawn_time = spawn_time
        self.current_time = 0
        self.is_can_spawn = True

    def create_new_target(self, a, b, z):
        target = Target(self.image_target, a, b, z, self.explosion_group, self.target_group)
        self.list.append(target)

    def destroy_target(self, target: Target):
        self.list.remove(target)
        self.used_coords.remove(target.get_coords())
        target.destroy()

    def get_target(self, a, b):
        pass

    def check_can_create_target(self, a, b):
        return (a, b) in self.used_coords

    def spawn_target(self):
        if self.is_can_spawn:
            pass

    def check_percent_field_occupancy(self):
        return self.get_percent_field_occupancy() <= MAX_PERSENT_FIELD_OCCUPANCY

    def get_percent_field_occupancy(self):
        count_fields = len(self.used_coords)
        return count_fields / (MAP_SIZE * MAP_SIZE)

    def reload_spawn(self, delta_t):
        self.current_time += delta_t
        if self.current_time >= self.spawn_time:
            self.is_can_spawn = True

    def target_generator(self):
        if self.check_percent_field_occupancy():
            if self.is_can_spawn:
                self.current_time = 0
                self.is_can_spawn = False
