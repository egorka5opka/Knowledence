import math
import pygame
from tools.methods import load_image, distance
from  const import colors, sizes


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health, *args):
        super().__init__(*args)
        self.max_health = max_health
        self.image = pygame.Surface(sizes.HEALTH_BAR_SIZE)
        self.image.fill(colors.NO_HEALTH_COLOR)
        self.rect = self.image.get_rect()
        health = pygame.Surface(sizes.HEALTH_BAR_SIZE)
        health.fill(colors.HEALTH_COLOR)
        self.image.blit(health, (0, 0))

    def move(self, rect):
        self.rect.bottom = rect.y
        self.rect.centerx = rect.centerx

    def update_health(self, hp):
        hbar = hp * sizes.HBAR_WIDTH / self.max_health
        health = pygame.Surface((hbar, sizes.HBAR_HEIGHT))
        health.fill(colors.HEALTH_COLOR)
        self.image.fill(colors.NO_HEALTH_COLOR)
        self.image.blit(health, (sizes.HBAR_WIDTH - hbar, 0))


class Enemy(pygame.sprite.Sprite):
    enemy_image = load_image("enemies/monster.png")
    enemy_image = pygame.transform.scale(enemy_image, (50, 50))

    def __init__(self, way_points, *args):
        super().__init__(*args)
        self.image = self.enemy_image
        self.rect = self.image.get_rect()
        self.velocity = 60
        self.buffs = {"velocity": 5, "damage": 1, "fly": False}
        self.hp = 100
        self.walked = 0
        self.way = way_points
        self.health_bar = HealthBar(self.hp, args[0])

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
        pass

    def update(self, tick, *args):
        self.health_bar.update_health(50)
        self.walked += self.velocity * self.buffs["velocity"] * tick / 1000
        self.calc_coords()


