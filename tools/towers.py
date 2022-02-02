import pygame
from tools.methods import load_image, load_tower, cut_sheet
from const import service, file_paths


class TowerPlace(pygame.sprite.Sprite):
    place_image = load_image("tower_place.png")

    def __init__(self, center, *groups):
        super().__init__(*groups)
        self.image = self.place_image
        self.rect = self.image.get_rect()
        self.rect.center = center


class Tower(pygame.sprite.Sprite):
    frames, damage, price, attack_speed, air,\
        damage_buf, velocity_buf, bullet_img, bullet_velocity = load_tower(file_paths.ARCHERY_TOWER, 1)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


