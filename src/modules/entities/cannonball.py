import pygame

from src.modules.base_classes.based.gravity_projectile import GravityProjectile


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
            z=0,
    ):
        super().__init__(start_speed, angle_height, angle_width, group, x=x, y=y, z=z)
        self.image = img

    def get_cords(self):
        return self.cord_x, self.cord_y, self.cord_z

    def draw(self, screen):
        pass


class ListCannonBalls:
    def __int__(self, start_speed, img):
        # noinspection PyCompatibility
        self.list_obj: list[CannonBall] = []
        self.start_speed = start_speed

        self.image = img

    def spawn_cannonball(self, angle_height, angle_width):
        self.list_obj.append(CannonBall(self.image, self.start_speed, angle_height, angle_width))

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
            obj.update(delta_t)

    def draw(self, screen):
        for obj in self.list_obj:
            obj.draw(screen)
