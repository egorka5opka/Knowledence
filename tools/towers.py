import pygame
from tools.methods import load_image, load_tower, tower_dist
from tools.classes import Bullet
from const import service, file_paths
import math


class TowerPlace(pygame.sprite.Sprite):
    place_image = load_image("tower_place.png")

    def __init__(self, center, *groups):
        super().__init__(*groups)
        self.image = self.place_image
        self.rect = self.image.get_rect()
        self.rect.center = center


class Tower(pygame.sprite.Sprite):
    frames, damage, price, attack_speed, air,\
        damage_buf, velocity_buf, bullet_img, bullet_velocity, attack_radius = load_tower(file_paths.ARCHERY_TOWER, 1)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.attack_centre = (x, y + TowerPlace.place_image.get_height() / 2)
        self.buffs = {service.DAMAGE_BUFF: 1, service.ATTACK_SPEED_BUFF: 1}
        self.delay = self.next_attack_time()

    def update(self, tick, enemies, entities, all_sprites, *args):
        if self.delay > 0:
            self.delay -= tick
        if self.delay <= 0:
            enemy = None
            dist = 0
            for e in enemies:
                if not enemy or dist > tower_dist(*self.attack_centre, e.rect):
                    enemy = e
                    dist = tower_dist(*self.attack_centre, e.rect)
            if enemy and dist <= self.attack_radius ** 2:
                self.attack(enemy, entities, all_sprites)
                self.delay = self.next_attack_time()

    def next_attack_time(self):
        return int(1 / self.attack_speed * self.buffs[service.ATTACK_SPEED_BUFF] * 1000)

    def attack(self, enemy, entities, all_sprites):
        Bullet(self.bullet_img, self.bullet_velocity, self.damage, self.rect.center, enemy,
               self.attack_radius, entities, all_sprites)



