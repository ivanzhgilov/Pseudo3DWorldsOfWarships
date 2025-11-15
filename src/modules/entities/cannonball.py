import pygame

from src.modules.base_classes.based.gravity_projectile import GravityProjectile

class CannonBall(GravityProjectile):
    def __init__(self, img, start_speed, angle_height, angle_width, target_group, *group, x=0, y=0, z=0):
        super().__init__(start_speed, angle_height, angle_width, group, x=x, y=y, z=z)
        self.image = img
        self.target_group = target_group

    def hit_target(self):

