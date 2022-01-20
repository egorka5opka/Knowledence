import pygame
from tools.methods import load_image


class TowerPlace(pygame.sprite.Sprite):
    place_image = load_image("tower_place.png")

    def __init__(self, center, *args):
        super().__init__(*args)
        # x = center - self.place_image.get_width() / 2
        # y = center - self.place_image.get_height() / 2
        self.image = self.place_image
        self.rect = self.image.get_rect()
        self.rect.center = center
