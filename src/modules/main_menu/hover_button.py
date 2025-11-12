import pygame
import src.consts

from src.utils.funcs import load_sound

BUTTON_WIDTH, BUTTON_HEIGHT = src.consts.BUTTON_WIDTH, src.consts.BUTTON_HEIGHT


class HoverButton(pygame.sprite.Sprite):
    def __init__(self, x, y, text, *group, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                 normal_color=(150, 150, 150), hover_color=(100, 100, 100),
                 text_color=(0, 0, 0), hover_text_color=(206, 115, 34),
                 border_color=(0, 0, 0), hover_border_color=(206, 115, 34),
                 border_width=2,
                 font_size=24):
        super().__init__(group)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

        # Основные параметры
        self.width = width
        self.height = height
        self.text = text

        # Цвета для разных состояний
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.border_color = border_color
        self.hover_border_color = hover_border_color
        self.border_width = border_width

        # Текущее состояние
        self.is_hovered = False

        # Шрифт для текста
        self.font = pygame.font.Font(None, font_size)

        # Первоначальная отрисовка
        self.draw()

    def draw(self):
        """Отрисовка кнопки на поверхности"""
        # Очистка поверхности
        self.image.fill((0, 0, 0, 0))

        # Выбор цветов в зависимости от состояния
        if self.is_hovered:
            bg_color = self.hover_color
            text_color = self.hover_text_color
            border_color = self.hover_border_color
        else:
            bg_color = self.normal_color
            text_color = self.text_color
            border_color = self.border_color

        # Отрисовка фона
        pygame.draw.rect(self.image, bg_color, (0, 0, self.width, self.height))

        # Отрисовка контура
        pygame.draw.rect(self.image, border_color, (0, 0, self.width, self.height), self.border_width)

        # Отрисовка текста
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def update(self):
        """Обновление состояния кнопки"""
        # Получаем позицию мыши
        mouse_pos = pygame.mouse.get_pos()

        self.is_hovered = self.rect.collidepoint(mouse_pos)

        self.draw()


# Пример использования
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Создание группы спрайтов
    all_sprites = pygame.sprite.Group()

    # Создание кнопки
    button = HoverButton(300, 250, "Нажми меня!")

    all_sprites.add(button)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button.is_hovered:
                    print(event.pos)
                    print(event.button)

        # Обновление кнопки
        button.update()


        # Отрисовка
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
