import pygame
from const import service


def run():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return service.QUIT
    return service.START_MENU
