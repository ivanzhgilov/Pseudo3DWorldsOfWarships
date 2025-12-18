import math
import sys

import pygame

import src.consts
from src.modules.base_classes.based.base_game import BaseGame
from src.modules.control_objects.control_targets_and_cannonballs import (
    ControlTargetsAndCannonballs,
)
from src.modules.entities.cannonball import ListCannonBalls
from src.modules.game_background.generation_background import Background
from src.modules.main_menu.start_screen import StartScreen
from src.modules.player.player import Player
from src.modules.target.target import ListTargets
from src.utils.funcs import load_image, load_sound

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


def func(timer, x):
    coef = (math.sin(x / 300 + timer)) * 50
    return coef


def func_2(timer):
    coef = math.sin(timer) * 5
    return coef


def start_game(main_screen: pygame.Surface, fps: int = 60):
    start = StartScreen(main_screen)
    start.start_screen()


class Game(BaseGame):
    def __init__(self, main_screen: pygame.Surface, fps: int = 60):
        super().__init__(main_screen, fps)
        self.bk = Background()
        self.list_cannon = ListCannonBalls(200)
        self.list_target = ListTargets(7)
        self.control = ControlTargetsAndCannonballs(self.list_target, self.list_cannon)
        self.player = Player(1, self.control)
        self.counter = 0

        self.timer = 0

        self.game_theme = load_sound("sounds/game/game_theme.mp3")

    def setup(self):
        self.register_event(pygame.MOUSEBUTTONDOWN, self.shot)
        self.register_event(pygame.QUIT, self.terminate)
        pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
        self.start_music()
        pygame.mouse.set_visible(False)

    def shot(self, event: pygame.event.Event):
        if event.button == 1:
            self.player.shot()

    def update(self, delta_t: float):
        self.counter += 1
        self.player.update(delta_t)
        self.control.update(delta_t)
        self.bk.change_angle(self.player.angle_height)
        if self.counter % 10 == 0:
            pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
            self.counter = 0
        self.timer += delta_t

    def draw(self, screen: pygame.Surface):
        self.bk.an_move = func_2(self.timer)
        self.bk.timer = self.timer
        self.bk.draw(screen)
        self.control.draw(screen, self.player.angle_width, self.player.angle_height)
        self.player.draw(screen)

    def start_music(self):
        self.game_theme.play(-1)

    def terminate(self, event: pygame.event.Event):
        pygame.quit()
        sys.exit()

    def shift_column_up(self, screen, x, shift_amount):
        y_start = 0
        y_end = HEIGHT

        segment_height = y_end - y_start

        segment_surface = pygame.Surface((1, segment_height), pygame.SRCALPHA)
        segment_surface.blit(screen, (0, 0), (x, y_start, 1, segment_height))

        pygame.draw.rect(screen, (0, 0, 0), (x, y_start, 1, segment_height))
        insert_y = y_start - shift_amount

        insert_im = load_image("images/game/floor.png")

        fill_surf = pygame.Surface((1, shift_amount), pygame.SRCALPHA)
        fill_surf.blit(insert_im, (0, 0), (0, 0, 1, shift_amount))

        if insert_y < 0:
            visible_height = segment_height + insert_y
            if visible_height > 0:
                screen.blit(segment_surface, (x, 0), (0, -insert_y, 1, visible_height))
        else:
            screen.blit(segment_surface, (x, insert_y))

        screen.blit(fill_surf, fill_surf.get_rect(topleft=(x, HEIGHT - shift_amount)))

    def wave_simulation(self, screen: pygame.Surface):
        for x in range(WIDTH):
            shift_y = max(0, func(self.timer, x))
            self.shift_column_up(screen, x, shift_y)
