import pygame
from tools.methods import load_image, load_tower, tower_dist
from tools.classes import Bullet, SupportCursor
from const import service, file_paths
import math


class TowerPlace(pygame.sprite.Sprite):
    place_image = load_image("tower_place.png")

    def __init__(self, center, *groups):
        super().__init__(*groups)
        self.image = self.place_image
        self.rect = self.image.get_rect()
        self.rect.center = center

    def click(self, cords, set_building):
        click = SupportCursor(*cords)
        res = bool(pygame.sprite.collide_rect(self, click))
        click.kill()
        if res:
            set_building(self)


class Tower(pygame.sprite.Sprite):
    frames, base_damage, price, attack_speed, air, damage_buf, velocity_buf, buffs_time, bullet_img, bullet_velocity,\
        base_attack_radius, icon, bullet_time = load_tower(file_paths.ARCHERY_TOWER, 1)
    damage_upgrade = 2.5
    speed_upgrade = 1.1
    damage_buf_upgrade = 1
    velocity_buf_upgrade = 1

    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.attack_centre = (x, y - TowerPlace.place_image.get_height() / 2)
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
                if e.flying and not self.air:
                    continue
                if (not enemy or walked < e.walked)\
                        and tower_dist(*self.attack_centre, e.rect) <= self.attack_radius ** 2:
                    enemy = e
                    walked = e.walked
            if enemy and tower_dist(*self.attack_centre, enemy.rect) <= self.attack_radius ** 2:
                if len(self.frames) > 1:
                    if enemy.rect.centerx <= self.rect.centerx:
                        self.image = self.frames[0]
                    else:
                        self.image = self.frames[1]
                self.attack(enemy, entities, all_sprites)
                self.delay = self.next_attack_time()

    def click(self, cords, set_panel):
        click = SupportCursor(*cords)
        res = bool(pygame.sprite.collide_rect(self, click))
        click.kill()
        if res:
            set_panel(self)

    def next_attack_time(self):
        return int(1 / self.attack_speed * self.buffs[service.ATTACK_SPEED_BUFF] * 1000)

    def attack(self, enemy, entities, all_sprites):
        buffs = [(service.VELOCITY_BUFF, self.velocity_buf, self.buffs_time),
                 (service.DAMAGE_BUFF, self.damage_buf, self.buffs_time)]
        Bullet(self.bullet_img, self.bullet_velocity, self.damage, self.rect.center, enemy,
               self.attack_radius + 100, self.bullet_time, buffs, entities, all_sprites)

    def upgrade(self, money):
        if money.get_money() < self.upgrade_price:
            return
        self.cost += self.upgrade_price
        money -= self.upgrade_price
        self.upgrade_price = int(self.upgrade_price * 1.8)
        self.damage *= self.damage_upgrade
        self.attack_speed *= self.speed_upgrade
        self.damage_buf *= self.damage_buf_upgrade
        self.velocity_buf *= self.velocity_buf_upgrade

    def sell(self, money, *place_groups):
        money += int(self.cost * 0.7)
        print(self.attack_centre)
        TowerPlace(self.attack_centre, *place_groups)
        self.kill()


class Cannon(Tower):
    frames, base_damage, price, attack_speed, air, damage_buf, velocity_buf, buffs_time, bullet_img, bullet_velocity, \
        base_attack_radius, icon, bullet_time = load_tower("data/towers_data/cannon.tower", 1)


tower_classes = {"archery": Tower, "cannon": Cannon}
