import pygame
from const import sizes, service, colors, file_paths
from tools import classes, methods


class Lives(pygame.sprite.Sprite):
    image = methods.load_image("resources.png")

    def __init__(self, points, *args):
        super().__init__(*args)
        self.points = points
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(1350, 0)

    def __iadd__(self, other):
        self.points -= other
        return self

    def __isub__(self, other):
        self.points -= other
        return self

    def get_points(self):
        return self.points
