import pygame
from const import service


def run(screen,  *args, **kwargs):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return service.QUIT
    return service.UPGRADING
