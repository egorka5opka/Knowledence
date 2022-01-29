import csv
import math
import pygame
from tools.methods import distance, load_enemy
from const.service import DAMAGE_BUFF, VELOCITY_BUFF, FLY_ABILITY
from const import colors, sizes, file_paths


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health, *args):
        super().__init__(*args)
        self.max_health = max_health
        self.image = pygame.Surface(sizes.HEALTH_BAR_SIZE)
        self.image.fill(colors.NO_HEALTH_COLOR)
        self.rect = self.image.get_rect()
        self.update_health(max_health)

    def move(self, rect):
        self.rect.bottom = rect.y
        self.rect.centerx = rect.centerx

    def update_health(self, hp):
        hbar = int(hp * sizes.HBAR_WIDTH / self.max_health)
        health = pygame.Surface((hbar, sizes.HBAR_HEIGHT))
        health.fill(colors.HEALTH_COLOR)
        self.image.fill(colors.NO_HEALTH_COLOR)
        self.image.blit(health, (sizes.HBAR_WIDTH - hbar, 0))


class Enemy(pygame.sprite.Sprite):
    enemy_image, max_health, velocity, flying = load_enemy(file_paths.BASE_ENEMY)
    enemy_image = pygame.transform.scale(enemy_image, (50, 50))

    def __init__(self, way_points, *args):
        super().__init__(*args)
        self.image = self.enemy_image
        self.rect = self.image.get_rect()
        self.buffs = {VELOCITY_BUFF: 1, DAMAGE_BUFF: 1, FLY_ABILITY: self.flying}
        self.hp = self.max_health
        self.walked = 0
        self.way = way_points
        self.health_bar = HealthBar(self.hp, args[0])
        self.list_buffs = []
        self.gone = False

    def calc_coords(self):
        walked = 0.0
        cur_p = 1
        next_seg = distance(self.way[cur_p], self.way[cur_p - 1])
        while cur_p < len(self.way) and walked + next_seg <= self.walked:
            walked += next_seg
            cur_p += 1
            if cur_p == len(self.way):
                break
            next_seg = distance(self.way[cur_p], self.way[cur_p - 1])
        if cur_p >= len(self.way):
            self.missed()
            return
        L = self.walked - walked
        angle = math.atan2(self.way[cur_p][1] - self.way[cur_p - 1][1], self.way[cur_p][0] - self.way[cur_p - 1][0])
        self.rect.bottom = math.sin(angle) * L + self.way[cur_p - 1][1]
        self.rect.centerx = math.cos(angle) * L + self.way[cur_p - 1][0]
        self.health_bar.move(self.rect)

    def missed(self):
        self.gone = True

    def update(self, tick, *args):
        self.walked += self.velocity * self.buffs[VELOCITY_BUFF] * tick / 1000
        self.calc_coords()
        for_delete = []
        for i in range(len(self.list_buffs)):
            self.list_buffs[i][2] -= tick
            if self.list_buffs[i][2] < 0:
                for_delete.append(i)
                b, v, t = self.list_buffs[i]
                self.buffs[b] -= v
        j = 0
        buffs = []
        for i in range(len(self.list_buffs)):
            if j < len(for_delete) and i == for_delete[j]:
                j += 1
                continue
            buffs.append(self.list_buffs[i])
        self.list_buffs = buffs

    def impact(self, hp_impact=0, *buffs):
        if hp_impact < 0:
            hp_impact *= self.buffs[DAMAGE_BUFF]
        self.hp += hp_impact
        self.hp = min(self.hp, self.max_health)
        if self.hp <= 0:
            self.kill()
        for b in buffs:
            self.buffs[b[0]] += b[1]
            self.list_buffs.append(list(b))
        self.health_bar.update_health(self.hp)

