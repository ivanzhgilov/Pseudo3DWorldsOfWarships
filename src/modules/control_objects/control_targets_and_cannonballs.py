import pygame

from src.modules.entities.cannonball import ListCannonBalls
from src.modules.target.target import ListTargets


class ControlTargetsAndCannonballs:
    def __init__(self, list_target: ListTargets, list_cannonballs: ListCannonBalls):
        self.list_targets = list_target
        self.list_cannonballs = list_cannonballs

    def check_hits(self):
        for cannonball in self.list_cannonballs.get_list():
            # noinspection PyCompatibility
            if (
                target := self.list_targets.get_collide(*cannonball.get_cords())
            ) is not None:
                if pygame.sprite.collide_circle(target, cannonball):
                    self.list_targets.destroy_target(target)
                    self.list_cannonballs.remove_cannonball(cannonball)

    def update(self, delta_t):
        self.check_hits()
        self.list_cannonballs.update(delta_t)
        self.list_targets.update(delta_t)

    def cannon_shot(self, angle_height, angle_width):
        self.list_cannonballs.spawn_cannonball(angle_height, angle_width)

    def draw(self, screen: pygame.surface.Surface, angle, h_angle):
        all_obj = self.list_targets.list_obj + self.list_cannonballs.list_obj
        all_obj.sort(key=lambda x: x.get_distance(), reverse=True)
        for obj in all_obj:
            obj.draw(screen, angle, h_angle)
