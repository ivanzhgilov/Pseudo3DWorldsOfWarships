import pygame

class MenuSprite(pygame.sprite.Sprite):

    def __init__(self, screen, img, x, y, rx, ry, *group):
        super().__init__(group)

        self.screen = screen
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.transform.smoothscale(self.image, (rx, ry))

        self.running = True
        self.action = None

    def update(self):
        pass
