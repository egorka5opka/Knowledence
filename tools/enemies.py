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
    file_name = file_paths.BASE_ENEMY
    frames, max_health, velocity, flying, price, reward = load_enemy(file_name, 1)
    frame_time = 180

    def __init__(self, way_points, *args):
        super().__init__(*args)
        self.frame = 0
        self.image = self.frames[0][0]
        self.next_frame = self.frame_time
        self.rect = self.image.get_rect()
        self.buffs = {VELOCITY_BUFF: 1, DAMAGE_BUFF: 1, FLY_ABILITY: self.flying}
        self.hp = self.max_health
        self.walked = 0
        self.way = way_points
        self.health_bar = HealthBar(self.hp, args[0])
        self.list_buffs = []
        self.gone = False
        self.mask = pygame.mask.from_surface(self.image)

    def calc_coords(self, length):
        walked = 0.0
        cur_p = 1
        next_seg = distance(self.way[cur_p], self.way[cur_p - 1])
        while cur_p < len(self.way) and walked + next_seg <= length:
            walked += next_seg
            cur_p += 1
            if cur_p == len(self.way):
                break
            next_seg = distance(self.way[cur_p], self.way[cur_p - 1])
        if cur_p >= len(self.way):
            self.missed()
            return self.rect.centerx, self.rect.bottom, 0
        L = length - walked
        angle = math.atan2(self.way[cur_p][1] - self.way[cur_p - 1][1], self.way[cur_p][0] - self.way[cur_p - 1][0])
        direction = int(self.way[cur_p][0] <= self.way[cur_p - 1][0])
        return math.cos(angle) * L + self.way[cur_p - 1][0], math.sin(angle) * L + self.way[cur_p - 1][1], direction

    def missed(self):
        self.gone = True

    def update(self, tick, *args):
        self.walked += self.velocity * self.buffs[VELOCITY_BUFF] * tick / 1000
        x, y, d = self.calc_coords(self.walked)
        self.rect.bottom = y
        self.rect.centerx = x
        self.health_bar.move(self.rect)
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

        self.next_frame -= tick
        if self.next_frame <= 0:
            self.frame += 1
            self.frame %= len(self.frames[0])
            self.next_frame = self.frame_time
            self.image = self.frames[d][self.frame]

    def will_walk(self, time):
        return self.walked + self.velocity * self.buffs[VELOCITY_BUFF] * time

    def impact(self, hp_impact=0, *buffs):
        if hp_impact < 0:
            hp_impact *= self.buffs[DAMAGE_BUFF]
        self.hp += hp_impact
        self.hp = max(min(self.hp, self.max_health), 0)
        for b in buffs:
            if b[1] == 0:
                continue
            self.buffs[b[0]] += b[1]
            self.list_buffs.append(list(b))
        self.health_bar.update_health(self.hp)


class Dude(Enemy):
    file_name = "data/enemies/dude.enemy"
    frames, max_health, velocity, flying, price, reward = load_enemy(file_name, 1)


class Griffon(Enemy):
    file_name = "data/enemies/griffon.enemy"
    frames, max_health, velocity, flying, price, reward = load_enemy(file_name, 1)
    frame_time = 120


class Hog(Enemy):
    file_name = "data/enemies/hog.enemy"
    frames, max_health, velocity, flying, price, reward = load_enemy(file_name, 1)
    frame_time = 100


class Shield(Enemy):
    file_name = "data/enemies/shield.enemy"
    frames, max_health, velocity, flying, price, reward = load_enemy(file_name, 1)


enemy_classes = {"base_enemy": Enemy, "dude": Dude, "griffon": Griffon, "hog": Hog, "shield": Shield}


def get_enemy_class(name):
    if name in enemy_classes:
        return enemy_classes[name]
    return Enemy
