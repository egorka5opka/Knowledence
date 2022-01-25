# файл с классами которые много где понадобятся
import pygame
from tools.methods import load_image


class SupportCursor(pygame.sprite.Sprite):
    def __init__(self, coordx, coordy):
        super().__init__()
        self.rect = pygame.Rect((coordx, coordy, 1, 1))
        self.image = pygame.Surface((1, 1))
        pygame.Surface.set_alpha(self.image, 0)


class Button(pygame.sprite.Sprite):
    def __init__(self, image_name, all_sprites, group_spr, coordx, coordy):
        super().__init__(all_sprites)
        self.add(group_spr)
        self.image = load_image(image_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.top = coordy
        self.rect.x = coordx

    def get_click(self, coordx, coordy):
        click = SupportCursor(coordx, coordy)
        if pygame.sprite.collide_rect(self, click):
            return True
        else:
            return False

    def move_on(self, x, y):
        self.rect.top += y
        self.rect.x += x


class Background(pygame.sprite.Sprite):
    def __init__(self, image_name, *groups):
        super().__init__(*groups)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0
