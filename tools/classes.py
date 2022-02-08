# файл с классами которые много где понадобятся
import pygame
from tools.methods import load_image, radians_to_degrees, distance
from math import sin, cos, atan2

class SupportCursor(pygame.sprite.Sprite):
    def __init__(self, coordx, coordy):
        super().__init__()
        self.rect = pygame.Rect((coordx, coordy, 1, 1))
        self.image = pygame.Surface((1, 1))
        pygame.Surface.set_alpha(self.image, 0)


class Button(pygame.sprite.Sprite):
    def __init__(self, image_name, coordx, coordy, *args):
        super().__init__(*args)
        self.image = load_image(image_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = coordy
        self.rect.x = coordx

    def get_click(self, coordx, coordy):
        click = SupportCursor(coordx, coordy)
        res = bool(pygame.sprite.collide_rect(self, click))
        click.kill()
        return res

    def move_on(self, x, y):
        self.rect.y += y
        self.rect.x += x


class Background(pygame.sprite.Sprite):
    def __init__(self, image_name, *groups):
        super().__init__(*groups)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, img, velocity, damage, start, enemy, radius, buffs, *groups):
        super().__init__(*groups)
        dist = distance(start, enemy.rect.center)
        finish = list(enemy.calc_coords(enemy.will_walk(dist / velocity)))
        finish[1] -= enemy.rect.height / 2
        dx = finish[0] - start[0]
        dy = finish[1] - start[1]
        angle = atan2(dy, dx)
        self.velocity = (velocity * cos(angle), velocity * sin(angle))
        self.velocity1 = velocity
        self.image = img
        self.image = pygame.transform.rotate(self.image, radians_to_degrees(-angle))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = start
        self.coords = list(start)
        self.damage = damage
        self.fin = finish
        self.radius = radius
        self.flew = 0
        self.buffs = buffs

    def update(self, tick, enemies, *args):
        self.coords[0] += self.velocity[0] * tick / 1000
        self.coords[1] += self.velocity[1] * tick / 1000
        self.flew += self.velocity1 * tick / 1000
        self.rect.center = self.coords
        for enemy in enemies:
            if pygame.sprite.collide_mask(enemy, self):
                enemy.impact(-self.damage, *self.buffs)
                self.kill()
        if self.flew >= self.radius:
            self.kill()
