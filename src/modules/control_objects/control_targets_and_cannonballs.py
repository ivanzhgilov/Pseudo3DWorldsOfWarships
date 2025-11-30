from src.modules.target.target import ListTarget
from src.modules.entities.cannonball import ListCannonBalls


class ControlTargetsAndCannonballs:
    def __init__(self, list_target: ListTarget, list_cannonballs: ListCannonBalls):
        self.list_target = list_target
        self.list_cannonballs = list_cannonballs


    def check_hits(self):
        for cannonball in self.list_cannonballs:
            # noinspection PyCompatibility
            if target := self.list_target.get_collide(*cannonball.get_cords()) is not None:
                self.list_target.destroy_target(target)
                self.list_cannonballs.remove_cannonball(cannonball)

    def update(self, delta_t):
        self.check_hits()
        self.list_cannonballs.update(delta_t)
        self.list_target.update(delta_t)

    def cannon_shot(self, angle_height, angle_width):
        self.list_cannonballs.spawn_cannonball(angle_height, angle_width)