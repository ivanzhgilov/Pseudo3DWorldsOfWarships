from __future__ import annotations

import math
import random

import pygame

import src.consts
from src.modules.target.explosion import Explosion
from src.utils.funcs import (
    get_cell_coords_from_coords,
    get_coords_from_cell,
    load_image,
)

MAP_SIZE = src.consts.MAP_SIZE
CELL_SIZE = src.consts.CELL_SIZE
RESERVED_CELLS, START_CAN_USE_CELLS = src.consts.RESERVED_CELLS, src.consts.START_CAN_USE_CELLS
MIN_Z, MAX_Z = src.consts.MIN_Z, src.consts.MAX_Z
MAX_PERSENT_FIELD_OCCUPANCY = src.consts.MAX_PERSENT_FIELD_OCCUPANCY
FOV_HALF_WIDTH, FOV_HALF_HEIGHT, FOV_INACCURACY = src.consts.FOV_HALF_WIDTH, src.consts.FOV_HALF_HEIGHT, src.consts.FOV_INACCURACY
WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT
COEF_MOVE_ANGLE = src.consts.COEF_MOVE_ANGLE


class Target(pygame.sprite.Sprite):
    def __init__(self, img: pygame.surface.Surface, a, b, z, *group, height_object=CELL_SIZE // 2):
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
        self.standart_size = [500, 500]
        self.rect = img.get_rect(center=self.standart_size)
        self.coef = COEF_MOVE_ANGLE

    def destroy(self):
        self.kill()
        Explosion(self.a, self.b, self.z).realize()

    def collide_cell(self, a, b):
        if a == self.a and b == self.b:
            return True
        return False

    def collide_height(self, z):
        if self.z_min + 3 <= z <= self.z_max - 3:
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

    def get_distance(self):
        x, y = get_coords_from_cell(self.a, self.b)
        return math.sqrt(x ** 2 + y ** 2 + self.z ** 2)

    def draw(self, screen, angle, h_angle):
        x, y = get_coords_from_cell(self.a, self.b)
        r = (x ** 2 + y ** 2) ** 0.5
        cos_a = x / r
        sin_a = y / r
        angle_right = angle - FOV_HALF_WIDTH - FOV_INACCURACY
        angle_left = angle + FOV_HALF_WIDTH + FOV_INACCURACY
        angle_up = h_angle + FOV_HALF_HEIGHT + FOV_INACCURACY
        angle_down = h_angle - FOV_HALF_HEIGHT - FOV_INACCURACY

        distance = (self.z ** 2 + r ** 2) ** 0.5

        sin_h = (self.z-10) / distance
        cur_h_an = math.asin(sin_h)

        if x * y > 0:
            if x > 0:
                cur_an = math.acos(cos_a)
            else:
                cur_an = -math.acos(cos_a) + 2 * math.pi
        else:
            if x < 0:
                cur_an = -math.asin(sin_a) + math.pi
            else:
                cur_an = math.asin(sin_a) + 2 * math.pi

        if angle_right < 0 and cur_an > math.pi:
            cur_an -= 2 * math.pi
        elif angle_left > 2 * math.pi and cur_an < math.pi:
            cur_an += 2 * math.pi

        if (angle_right <= cur_an <= angle_left) and angle_down <= cur_h_an <= angle_up:
            coef = 35 / distance
            size_w = self.standart_size[0] * coef
            size_h = self.standart_size[1] * coef
            img = pygame.transform.smoothscale(self.image, (size_w, size_h))
            diff_h = h_angle - cur_h_an
            cord_y = int(HEIGHT // 2 + (diff_h / FOV_HALF_HEIGHT) * (HEIGHT // 2))
            diff_angle = angle - cur_an
            cord_x = int(WIDTH // 2 + (diff_angle / FOV_HALF_WIDTH) * (WIDTH // 2))

            screen.blit(img, img.get_rect(center=(cord_x, cord_y)))
            self.rect = img.get_rect(center=(cord_x, cord_y))


class ListTargets:
    def __init__(self, spawn_time):
        # noinspection PyCompatibility
        self.list_obj: list[Target] = []
        # noinspection PyCompatibility
        self.used_coords: list[tuple[int, int]] = RESERVED_CELLS
        # noinspection PyCompatibility
        self.can_use_coords: list[tuple[int, int]] = START_CAN_USE_CELLS
        self.image_target = load_image("images/game/target.png")
        self.spawn_time = spawn_time
        self.current_time = 0
        self.is_can_spawn = False

    def create_new_target(self, a, b, z):
        target = Target(self.image_target, a, b, z)
        self.list_obj.append(target)
        self.used_coords.append((a, b))

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

    def get_collide(self, x, y, z) -> None | Target:
        a, b = get_cell_coords_from_coords(x, y)
        for target in self.list_obj:
            if target.collide(a, b, z):
                return target
        return None

    def update(self, delta_t):
        self.reload_spawn(delta_t)
        self.target_generator()
        for target in self.list_obj:
            target.update(delta_t)

    def draw(self, screen, angle, h_angle):
        for target in self.list_obj:
            target.draw(screen, angle, h_angle)
