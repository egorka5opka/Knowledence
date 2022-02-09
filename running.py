# В этом файле происходит запуск, и основной цикл while running
# Уже в нём вызываются функции из отдельных файлов в зависимости от того что сейчас происходит в игре

import pygame
pygame.init()
from const import service, sizes
screen = pygame.display.set_mode(sizes.WINDOW_SIZE)
import start_menu, main_menu, level_play, upgrading


def main():
    actions = {service.START_MENU: start_menu.run,
               service.MAIN_MENU: main_menu.run,
               service.LEVEL_PLAY: level_play.run,
               service.UPGRADING: upgrading.run}
    # функция run обрабатывает одну активность и возвращает какая активность будет следующей
    cur_action = service.START_MENU
    # cur_action = service.LEVEL_PLAY
    while cur_action != service.QUIT:
        cur_action = actions[cur_action](screen)


main()
