import pygame
from const import service
from tools import classes, methods

started = False
level = 0
all_sprites = pygame.sprite.Group()


def run(screen,  *args, **kwargs):
    global level
    level = 1
    load_level(all_sprites)
    running = service.LEVEL_PLAY
    while running == service.LEVEL_PLAY:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = service.QUIT
                break
        all_sprites.draw(screen)
        pygame.display.flip()
    all_sprites.clear()
    return running


def set_level(x):
    global level
    level = x


def load_level(all_sprites):
    background = classes.Background(f"levels_data/{level}level_background.png", all_sprites)

