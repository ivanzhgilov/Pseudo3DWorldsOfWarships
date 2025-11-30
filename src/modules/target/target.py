from __future__ import annotations

import random

import pygame

import src.consts
from src.modules.target.explosion import Explosion

MAP_SIZE = src.consts.MAP_SIZE
CELL_SIZE = src.consts.CELL_SIZE
RESERVED_CELLS, START_CAN_USE_CELLS = src.consts.RESERVED_CELLS, src.consts.START_CAN_USE_CELLS
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
        self.z = z
        self.z_min = z - height_object
        self.z_max = z + height_object
        self.explosion_group = explosion_group

    def destroy(self):
        self.kill()
        explosion = Explosion(self.a, self.b, self.z, self.explosion_group)
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

    def update(self, delta_t):
        pass

    def draw(self, screen):
        pass


class ListTarget:
    def __init__(self, spawn_time, img_target, explosion_group: pygame.sprite.Group):
        # noinspection PyCompatibility
        self.list_obj: list[Target] = []
        # noinspection PyCompatibility
        self.used_coords: list[tuple[int, int]] = RESERVED_CELLS
        # noinspection PyCompatibility
        self.can_use_coords: list[tuple[int, int]] = START_CAN_USE_CELLS
        self.explosion_group = explosion_group
        self.image_target = img_target
        self.spawn_time = spawn_time
        self.current_time = 0
        self.is_can_spawn = True

    def create_new_target(self, a, b, z):
        target = Target(self.image_target, a, b, z, self.explosion_group)
        self.list_obj.append(target)
        self.used_coords.append((a, b))
        self.can_use_coords.remove((a, b))

    def destroy_target(self, target: Target):
        self.list_obj.remove(target)
        self.used_coords.remove(target.get_coords())
        self.can_use_coords.append(target.get_coords())
        target.destroy()

    def get_target(self, a, b):
        pass

    def spawn_target(self):
        a, b = random.choice(self.can_use_coords)
        self.can_use_coords.remove((a, b))
        self.used_coords.append((a, b))
        z = random.randint(MIN_Z, MAX_Z)
        self.create_new_target(a, b, z)

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
        if self.is_can_spawn:
            if self.check_percent_field_occupancy():
                self.spawn_target()
            self.is_can_spawn = False
            self.current_time = 0

    def get_collide(self, a, b, z) -> None | Target:
        for target in self.list_obj:
            if target.collide(a, b, z):
                return target
        return None

    def update(self, delta_t):
        self.reload_spawn(delta_t)
        self.target_generator()
        for target in self.list_obj:
            target.update(delta_t)

    def draw(self, screen):
        for target in self.list_obj:
            target.draw(screen)

