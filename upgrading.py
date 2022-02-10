import pygame
from const import service
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from const.file_paths import UPGRADING_BACKGROUND, CLOSE_BUTTON, UPGRADE_BUTTON
from tools.methods import load_image
from tools.classes import Button
import csv
from const.service import UPGR_BUTT_ORDER
import tools.interface


def run(screen, *args, **kwargs):
    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()
    upgrading_button = pygame.sprite.Group()

    count = open("data/progress.txt", 'r')
    count.readline()
    count.readline()
    count = int(count.readline())

    stars = tools.interface.Stars(count, all_sprites)

    try:
        with open("data/upgrading_coords.csv") as fin:
            reader = csv.reader(fin, delimiter=";")
            coords_upgrading = [(int(i[0]), int(i[1])) for i in reader]
    except Exception as e:
        print("Не удалось загрузить улучшения: " + str(e))

    background = load_image(UPGRADING_BACKGROUND)
    close_button = Button(CLOSE_BUTTON, 1490, 20, all_sprites, button_sprites)
    for i in range(len(coords_upgrading)):
        Button(UPGRADE_BUTTON, coords_upgrading[i][0], coords_upgrading[i][1], all_sprites, upgrading_button)

    up_coord = 0
    screen.blit(background, (0, up_coord))
    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return service.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    # колесо вверх
                    up_coord = min(0, up_coord + 50)
                    for ind, spr in enumerate(upgrading_button):
                        spr.rect.top = min(coords_upgrading[ind][1], spr.rect.top + 50)
                elif event.button == 5:
                    up_coord = max(-350, up_coord - 50)
                    for ind, spr in enumerate(upgrading_button):
                        spr.rect.top = max(-350 + coords_upgrading[ind][1], spr.rect.top - 50)
                elif close_button.get_click(event.pos[0], event.pos[1]):
                    return service.MAIN_MENU
                else:
                    for ind, spr in enumerate(upgrading_button):
                        if spr.get_click(event.pos[0], event.pos[1]):
                            if count == 0:
                                break
                            type_tower = ind // 3
                            type_upgr = ind % 3
                            file = open(UPGR_BUTT_ORDER[type_tower], "r")
                            reader = csv.DictReader(file, delimetr=';')
                            tower = reader.__next__()
                            fin.close()
                            count -= 1
                            stars -= 1
                            if type_upgr == 0:
                                tower[service.ATTACK_RADIUS] += 5
                            elif type_upgr == 1:
                                tower[service.DAMAGE] += 5
                            else:
                                tower[service.ATTACK_SPEED] += 5

                            file = open(UPGR_BUTT_ORDER[type_tower], "w")
                            writer = csv.DictWriter(file, filednames=list(tower.keys()), delimiter=";")
                            writer.writeheader()
                            writer.write(tower)

        screen.blit(background, (0, up_coord))
        all_sprites.draw(screen)
        pygame.display.flip()
