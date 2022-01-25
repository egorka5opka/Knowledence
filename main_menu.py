import pygame
from const import service
from const.file_paths import MAP_BACKGROUND, SETTINGS_BUTTON, ENCYCLOPEDIA_BUTTON, UPGRADING_BUTTON, HOME_BUTTON, \
    COMPLETE_LEVEL, INCOMPLETE_LEVEL, LAUNCH_BACKGROUND, PLAY_BUTTON, CLOSE_BUTTON, LEVEL_BACKGROUND
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from tools.methods import load_image
from tools.classes import Button
import csv
from level_play import set_level


def run(screen, *args, **kwargs):
    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()
    levels_sprites = pygame.sprite.Group()

    try:
        with open("data/levels_coords.csv") as fin:
            reader = csv.reader(fin, delimiter=";")
            coords_levels = [(int(i[0]), int(i[1])) for i in reader]
    except Exception as e:
        print("Не удалось загрузить уровни: " + str(e))
    kol = open("data/progress.txt", mode='r')
    kol = int(kol.readline())

    # fon = pygame.transform.scale(load_image(MAP_BACKGROUND), (WINDOW_WIDTH, WINDOW_HEIGHT))
    fon = load_image(MAP_BACKGROUND)
    settings_button = Button(SETTINGS_BUTTON, all_sprites, button_sprites, 1380, 10)
    home_button = Button(HOME_BUTTON, all_sprites, button_sprites, 1462, 10)
    encyclopedia_button = Button(ENCYCLOPEDIA_BUTTON, all_sprites, button_sprites, 1140, 640)
    upgrading_button = Button(UPGRADING_BUTTON, all_sprites, button_sprites, 1365, 640)

    for i in range(kol):
        Button(COMPLETE_LEVEL, all_sprites, levels_sprites, coords_levels[i][0], coords_levels[i][1])
    if kol != 10:
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
                for ind, spr in enumerate(levels_sprites):
                    if spr.get_click(event.pos[0], event.pos[1]):
                        return launch(screen, ind)
        pygame.display.flip()


def launch(screen, level):
    SELF_WIDTH, SELF_HEIGHT = 742, 447

    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()

    fon = pygame.transform.scale(load_image(LAUNCH_BACKGROUND), (SELF_WIDTH, SELF_HEIGHT))
    map_of_level = pygame.transform.scale(load_image(LEVEL_BACKGROUND.format(level)), (465, 240))
    play_button = Button(PLAY_BUTTON, all_sprites, button_sprites, (WINDOW_WIDTH - 95) // 2, 550)
    close_button = Button(CLOSE_BUTTON, all_sprites, button_sprites, 1090, 190)

    screen.blit(fon, ((WINDOW_WIDTH - SELF_WIDTH) // 2, (WINDOW_HEIGHT - SELF_HEIGHT) // 2))
    screen.blit(map_of_level, ((WINDOW_WIDTH - SELF_WIDTH) // 2 + 30, (WINDOW_HEIGHT - SELF_HEIGHT) // 2 + 30))
    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return service.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.get_click(event.pos[0], event.pos[1]):
                    set_level(level)
                    return service.LEVEL_PLAY
                elif close_button.get_click(event.pos[0], event.pos[1]):
                    return service.MAIN_MENU
        pygame.display.flip()