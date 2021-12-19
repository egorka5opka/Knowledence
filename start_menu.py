import pygame
from const import service
from tools.methods import *


def run(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return service.QUIT
    pygame.display.flip()
    return service.START_MENU
