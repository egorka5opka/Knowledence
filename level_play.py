import pygame
from const import service

started = False
level = 0


def run(screen,  *args, **kwargs):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return service.QUIT
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(str(level), False, (130, 130, 130))
    screen.blit(text, (0, 0))
    pygame.display.flip()
    return service.LEVEL_PLAY


def set_level(x):
    global level
    level = x