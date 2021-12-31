import pygame
from const import service


def run(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return service.QUIT
    screen.fill((0, 0, 0))
    pygame.display.flip()
    return service.MAIN_MENU
