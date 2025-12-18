import math

import pygame

import src.consts
from src.utils.funcs import load_image

WIGHT, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT
COEF_MOVE_ANGLE = src.consts.COEF_MOVE_ANGLE


class Background:
    def __init__(self):
        self.angle_height = 0
        self.color_water = (23, 7, 218)
        self.color_sky = (156, 217, 252)
        self.color_cavity = (14, 4, 124)
        self.rect_water = pygame.Rect(0, 0, WIGHT, HEIGHT // 2)
        self.rect_sky = pygame.Rect(0, HEIGHT // 2, WIGHT, HEIGHT // 2)
        self.coef = COEF_MOVE_ANGLE
        self.h_sky = HEIGHT // 2 * 1.2
        self.h_water = HEIGHT // 2 * 0.8
        self.floor = load_image("images/game/floor.png")
        self.an_move = 0
        self.timer = 0

    def change_angle(self, angle):
        self.angle_height = angle
        h_water = int(HEIGHT // 2 * 0.8 - math.sin(angle) * self.coef)
        h_sky = HEIGHT - h_water
        self.rect_water = pygame.Rect(0, h_sky, WIGHT, h_water)
        self.rect_sky = pygame.Rect(0, 0, WIGHT, h_sky)
        self.h_sky = h_sky
        self.h_water = h_water

    def update(self, delta_t):
        pass

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, self.color_water, self.rect_water)
        pygame.draw.rect(screen, self.color_sky, self.rect_sky)
        self.draw_diagonal_stripes(screen, 5)
        in_fl = pygame.transform.rotate(self.floor, self.an_move)
        screen.blit(in_fl, in_fl.get_rect(center=(WIGHT // 2, HEIGHT + 50)))

    def draw_diagonal_stripes(self, surface, stripe_width):
        draw_height = self.h_water
        angle_rad = math.radians(30)
        line_length = draw_height / math.sin(angle_rad)

        offset_x = -line_length - self.timer * 100

        while offset_x < WIGHT:
            start_x = offset_x
            start_y = HEIGHT

            end_x = start_x + line_length * math.cos(angle_rad)
            end_y = start_y - line_length * math.sin(angle_rad) + 5

            pygame.draw.line(
                surface,
                self.color_cavity,
                (start_x, start_y),
                (end_x, end_y),
                stripe_width,
            )

            offset_x += 50
