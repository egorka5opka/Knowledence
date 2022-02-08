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
    frames, base_damage, price, attack_speed, air, damage_buf, velocity_buf, buffs_time, bullet_img, bullet_velocity,\
        base_attack_radius = load_tower(file_paths.ARCHERY_TOWER, 1)

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.attack_centre = (x, y + TowerPlace.place_image.get_height() / 2)
        self.buffs = {service.DAMAGE_BUFF: 1, service.ATTACK_SPEED_BUFF: 1}
        self.delay = self.next_attack_time()
        self.cost = self.price
        self.upgrade_price = int(self.cost * 1.8)
        self.damage = self.base_damage
        self.attack_radius = self.base_attack_radius

    def update(self, tick, enemies, entities, all_sprites, *args):
        if self.delay > 0:
            self.delay -= tick
        if self.delay <= 0:
            enemy = None
            walked = 0
            for e in enemies:
                if (not enemy or walked < e.walked)\
                        and tower_dist(*self.attack_centre, e.rect) <= self.attack_radius ** 2:
                    enemy = e
                    walked = e.walked
            if enemy and tower_dist(*self.attack_centre, enemy.rect) <= self.attack_radius ** 2:
                if len(self.frames) > 1 and enemy.rect.centerx <= self.rect.centerx:
                    self.image = self.frames[0]
                else:
                    self.image = self.frames[1]
                self.attack(enemy, entities, all_sprites)
                self.delay = self.next_attack_time()

    def next_attack_time(self):
        return int(1 / self.attack_speed * self.buffs[service.ATTACK_SPEED_BUFF] * 1000)

    def attack(self, enemy, entities, all_sprites):
        buffs = [(service.VELOCITY_BUFF, self.velocity_buf, self.buffs_time),
                 (service.DAMAGE_BUFF, self.damage_buf, self.buffs_time)]
        Bullet(self.bullet_img, self.bullet_velocity, self.damage, self.rect.center, enemy,
               self.attack_radius + 100, buffs, entities, all_sprites)

    def upgrade(self):
        self.cost += self.upgrade_price


tower_classes = {"archery": Tower}

