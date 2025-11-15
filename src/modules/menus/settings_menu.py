import sys

import pygame

import src.consts
from src.modules.base_classes.menu.menu_sprite import MenuSprite
from src.modules.base_classes.menu.hover_button import HoverButton
from src.utils.funcs import load_image

BUTTON_WIDTH, BUTTON_HEIGHT = src.consts.BUTTON_WIDTH, src.consts.BUTTON_HEIGHT
WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT


class SettingsMenu(MenuSprite):
    def __init__(
        self, screen, img, x, y, rx, ry, start_button_x, start_button_y, *group
    ):
        super().__init__(screen, img, x, y, rx, ry, *group)
        self.buttons = pygame.sprite.Group()
        self.button_example = HoverButton(
            start_button_x, start_button_y, "Пример", self.buttons
        )
        self.button_quit = HoverButton(
            start_button_x,
            start_button_y + BUTTON_HEIGHT + 10 + 130,
            "Выход",
            self.buttons,
        )

    def start_menu(self):
        clock = pygame.time.Clock()
        fon = pygame.transform.smoothscale(
            load_image("images/menu/shadow_background.png"), (WIDTH, HEIGHT)
        )
        self.screen.blit(fon, (0, 0))
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        while self.running:
            self.handle_event()
            self.update()
            self.draw()

            pygame.display.flip()
            clock.tick(src.consts.FPS)

        self.quit()

    def update(self):
        self.buttons.update()
        self.do_action()

    def draw(self):
        self.buttons.draw(self.screen)

    def handle_event(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button = self.clicked_button()
                if button == "quit":
                    self.quit()
                self.action = button
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def clicked_button(self):
        if self.button_example.is_hovered:
            return "example"
        elif self.button_quit.is_hovered:
            return "quit"
        return None

    def quit(self):
        self.running = False

    def do_action(self):
        if self.action == "example":
            self.example()

        self.action = None

    def example(self):
        print("example")
