import pygame
from const import service
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from const.file_paths import LAUNCH_BACKGROUND
from tools.methods import load_image
from tools.classes import Button


def run(screen,  *args, **kwargs):
    background = pygame.transform.scale(load_image(LAUNCH_BACKGROUND), (WINDOW_WIDTH, WINDOW_HEIGHT))

    screen.blit(background, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return service.QUIT
        pygame.display.flip()

