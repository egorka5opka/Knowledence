# файл с классами которые много где понадобятся
import pygame
from tools.methods import load_image

class Vspom_kursor(pygame.sprite.Sprite):
    def __init__(self, coordx, coordy):
        super().__init__()
        self.image = load_image("kursor_empty.png")
        self.mask = pygame.mask.from_surface(load_image("kursor_mask.png"))
        self.rect = self.image.get_rect()
        self.rect.top = coordy
        self.rect.x = coordx

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
        kur = Vspom_kursor(coordx, coordy)
        if pygame.sprite.collide_mask(self, kur):
            return True
        else:
            return False
