import pygame
from const import service
from const.file_paths import MAP_BACKGROUND, SETTINGS_BUTTON, ENCYCLOPEDIA_BUTTON, UPGRADING_BUTTON, HOME_BUTTON
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from tools.methods import load_image
from tools.classes import Button


def run(screen):
    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()

    fon = pygame.transform.scale(load_image(MAP_BACKGROUND), (WINDOW_WIDTH, WINDOW_HEIGHT))
    settings_button = Button(SETTINGS_BUTTON, all_sprites, button_sprites, 1360, 10)
    home_button = Button(HOME_BUTTON, all_sprites, button_sprites, 1460, 10)
    encyclopedia_button = Button(ENCYCLOPEDIA_BUTTON, all_sprites, button_sprites, 1140, 640)
    upgrading_button = Button(UPGRADING_BUTTON, all_sprites, button_sprites, 1365, 640)

    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return service.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if settings_button.get_click(event.pos[0], event.pos[1]):
                    pass
                elif home_button.get_click(event.pos[0], event.pos[1]):
                    return service.START_MENU
                elif encyclopedia_button.get_click(event.pos[0], event.pos[1]):
                    pass
                elif upgrading_button.get_click(event.pos[0], event.pos[1]):
                    pass
        pygame.display.flip()

