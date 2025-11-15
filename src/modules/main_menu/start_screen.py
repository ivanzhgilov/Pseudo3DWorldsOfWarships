import sys

import pygame

import src.consts
from src.modules.base_classes.menu.hover_button import HoverButton
from src.modules.menus.quit_menu import QuitMenu
from src.modules.menus.settings_menu import SettingsMenu
from src.utils.funcs import load_image, load_sound

WIDTH, HEIGHT = src.consts.WIDTH, src.consts.HEIGHT
BUTTON_WIDTH, BUTTON_HEIGHT = src.consts.BUTTON_WIDTH, src.consts.BUTTON_HEIGHT
START_BUTTON_X, START_BUTTON_Y = src.consts.START_BUTTON_X, src.consts.START_BUTTON_Y


class StartScreen:
    def __init__(self, screen):
        self.screen = screen

        self.running = True
        self.next_screen = None
        self.buttons = pygame.sprite.Group()
        self.button_play = HoverButton(
            START_BUTTON_X, START_BUTTON_Y, "Играть", self.buttons
        )
        self.button_settings = HoverButton(
            START_BUTTON_X,
            START_BUTTON_Y + BUTTON_HEIGHT + 10,
            "Настройки",
            self.buttons,
        )
        self.button_quit = HoverButton(
            START_BUTTON_X,
            START_BUTTON_Y + 2 * BUTTON_HEIGHT + 20,
            "Выход",
            self.buttons,
        )

        self.sound_start = load_sound("sounds/menu/start_game.mp3")
        self.sound_settings = load_sound("sounds/menu/button_click.mp3")
        self.sound_quit = load_sound("sounds/menu/button_click.mp3")

        self.sound_main = load_sound("sounds/menu/button_click.mp3")

        self.menu_theme = load_sound("sounds/menu/menu_theme.mp3")
        self.menu_theme.set_volume(0.3)

    def update(self):
        self.buttons.update()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def clicked_button(self):
        if self.button_play.is_hovered:
            return "play"
        elif self.button_settings.is_hovered:
            return "settings"
        elif self.button_quit.is_hovered:
            return "quit"
        return None

    def handle_event(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button = self.clicked_button()
                if not (button is None):
                    self.next_screen = button
                    self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.next_screen = "quit"
                self.running = False

    def start_screen(self):
        clock = pygame.time.Clock()
        fon = pygame.transform.smoothscale(
            load_image("images/menu/main_background.png"), (WIDTH, HEIGHT)
        )
        self.screen.blit(fon, (0, 0))
        while self.running:
            self.handle_event()
            self.update()
            self.draw()

            pygame.display.flip()
            clock.tick(src.consts.FPS)

        self.switch_menu()

    def draw(self):
        self.buttons.draw(self.screen)

    def switch_menu(self):
        self.running = True
        if self.next_screen == "quit":
            self.start_quit_menu()
        elif self.next_screen == "settings":
            self.start_settings_menu()
        elif self.next_screen == "play":
            self.start_play()

    def start_settings_menu(self):
        self.sound_settings.play()
        settings_menu = SettingsMenu(
            self.screen,
            load_image("images/menu/settings_menu.png"),
            150,
            0,
            1140,
            960,
            400,
            400,
        )
        settings_menu.start_menu()

        self.sound_main.play()
        self.start_screen()

    def start_quit_menu(self):
        self.sound_quit.play()
        quit_menu = QuitMenu(
            self.screen,
            load_image("images/menu/quit_menu.png"),
            320,
            0,
            800,
            960,
            620,
            550,
        )
        quit_menu.start_menu()

        self.sound_main.play()
        self.start_screen()

    def start_play(self):
        self.sound_start.play()
        print(12)
        return 1

    def start_music(self):
        self.menu_theme.play(-1)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1440, 960))
    main_menu = StartScreen(screen)
    main_menu.start_screen()
