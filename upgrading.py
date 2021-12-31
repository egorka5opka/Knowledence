import pygame
from const import service


def run(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return service.QUIT
    return service.UPGRADING
