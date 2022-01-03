import pygame
from const import service
from const.file_paths import MAP_BACKGROUND, SETTINGS_BUTTON, ENCYCLOPEDIA_BUTTON, UPGRADING_BUTTON, HOME_BUTTON, \
    COMPLETE_LEVEL, INCOMPLETE_LEVEL
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from tools.methods import load_image
from tools.classes import Button


def run(screen):
    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()
    levels_sprites = pygame.sprite.Group()

    coords_levels = [(320, 405), (380, 450), (455, 410), (525, 365), (615, 370), (685, 410), (740, 460),
                     (820, 470), (900, 490), (965, 450)]
    kol = open("data/progress.txt", mode='r')
    kol = int(kol.readline())

    fon = pygame.transform.scale(load_image(MAP_BACKGROUND), (WINDOW_WIDTH, WINDOW_HEIGHT))
    settings_button = Button(SETTINGS_BUTTON, all_sprites, button_sprites, 1380, 10)
    home_button = Button(HOME_BUTTON, all_sprites, button_sprites, 1462, 10)
    encyclopedia_button = Button(ENCYCLOPEDIA_BUTTON, all_sprites, button_sprites, 1140, 640)
    upgrading_button = Button(UPGRADING_BUTTON, all_sprites, button_sprites, 1365, 640)

    for i in range(kol):
        Button(COMPLETE_LEVEL, all_sprites, levels_sprites, coords_levels[i][0], coords_levels[i][1])
    Button(INCOMPLETE_LEVEL, all_sprites, levels_sprites, coords_levels[kol][0], coords_levels[kol][1])

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
                for spr in levels_sprites:
                    if spr.get_click(event.pos[0], event.pos[1]):
                        pass
        pygame.display.flip()
