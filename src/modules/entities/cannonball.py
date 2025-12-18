import math

import pygame

import src.consts
from src.modules.base_classes.based.gravity_projectile import GravityProjectile
from src.utils.funcs import get_coords_from_cell, load_image

FOV_HALF_WIDTH, FOV_HALF_HEIGHT, FOV_INACCURACY = (
    src.consts.FOV_HALF_WIDTH,
    src.consts.FOV_HALF_HEIGHT,
    src.consts.FOV_INACCURACY,
)
WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


class CannonBall(GravityProjectile):
    def __init__(
        self,
        img,
        start_speed,
        angle_height,
        angle_width,
        *group,
        x=0,
        y=0,
        z=10,
    ):
        super().__init__(start_speed, angle_height, angle_width, group, x=x, y=y, z=z)
        self.image = img
        self.standart_size = [100, 100]
        self.rect = self.image.get_rect()

    def get_cords(self):
        return self.cord_x, self.cord_y, self.cord_z

    def draw(self, screen, angle, h_angle):
        if not self.is_fallen:
            x, y, z = self.get_cords()
            r = (x**2 + y**2) ** 0.5
            cos_a = x / r
            sin_a = y / r
            angle_right = angle - FOV_HALF_WIDTH - FOV_INACCURACY
            angle_left = angle + FOV_HALF_WIDTH + FOV_INACCURACY
            angle_up = h_angle + FOV_HALF_HEIGHT + FOV_INACCURACY
            angle_down = h_angle - FOV_HALF_HEIGHT - FOV_INACCURACY

            distance = (z**2 + r**2) ** 0.5

            sin_h = (z - 10) / distance
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

            if (
                angle_right <= cur_an <= angle_left
                and angle_down <= cur_h_an <= angle_up
            ):
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

    def update(self, delta_t):
        super().update(delta_t)

    def get_distance(self):
        return math.sqrt(self.cord_x**2 + self.cord_y**2 + self.cord_z**2)


class ListCannonBalls:
    def __init__(self, start_speed: float):
        # noinspection PyCompatibility
        self.list_obj: list[CannonBall] = []
        self.start_speed = start_speed

        self.image = load_image("images/game/cannonball.png")

    def spawn_cannonball(self, angle_height, angle_width):
        self.list_obj.append(
            CannonBall(self.image, self.start_speed, angle_height, angle_width)
        )

    def get_all_cords(self):
        res = []
        for obj in self.list_obj:
            res.append(obj.get_cords())
        return res

    def get_list(self):
        return self.list_obj

    def remove_cannonball(self, cannonball: CannonBall):
        cannonball.delete_projectile()
        self.list_obj.remove(cannonball)

    def update(self, delta_t):
        for obj in self.list_obj:
            if obj.is_fallen:
                self.remove_cannonball(obj)
            obj.update(delta_t)

    def draw(self, screen, angle, h_angle):
        for obj in self.list_obj:
            obj.draw(screen, angle, h_angle)
