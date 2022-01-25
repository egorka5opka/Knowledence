import math

import pygame
from tools.methods import load_image, distance


class Enemy(pygame.sprite.Sprite):
    enemy_image = load_image("enemies/monster.png")
    enemy_image = pygame.transform.scale(enemy_image, (80, 80))

    def __init__(self, way_points, *args):
        super().__init__(*args)
        self.image = self.enemy_image
        self.rect = self.image.get_rect()
        self.velocity = 60
        self.hp = 100
        self.walked = 0
        self.way = way_points

    def calc_coords(self):
        walked = 0.0
        cur_p = 1
        next_seg = distance(self.way[cur_p], self.way[cur_p - 1])
        while cur_p < len(self.way) and walked + next_seg <= self.walked:
            walked += next_seg
            cur_p += 1
            next_seg = distance(self.way[cur_p], self.way[cur_p - 1])
        L = self.walked - walked
        if cur_p == len(self.way):
            self.missed()
            return
        angle = math.atan2(self.way[cur_p][1] - self.way[cur_p - 1][1], self.way[cur_p][0] - self.way[cur_p - 1][0])
        self.rect.x = math.cos(angle) * L + self.way[cur_p - 1][0]
        self.rect.y = math.sin(angle) * L + self.way[cur_p - 1][1]
        print(self.rect.x, self.rect.y)

    def missed(self):
        pass

    def update(self, tick, *args):
        self.walked += self.velocity * tick / 1000
        self.calc_coords()
