import pygame
from const import service
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from const.file_paths import UPGRADING_BACKGROUND, CLOSE_BUTTON
from tools.methods import load_image
from tools.classes import Button


def run(screen,  *args, **kwargs):
    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()

    background = pygame.transform.scale(load_image(UPGRADING_BACKGROUND), (WINDOW_WIDTH, WINDOW_HEIGHT))
    close_button = Button(CLOSE_BUTTON, all_sprites, button_sprites, 1490, 20)

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return service.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.get_click(event.pos[0], event.pos[1]):
                    return service.MAIN_MENU
        pygame.display.flip()

