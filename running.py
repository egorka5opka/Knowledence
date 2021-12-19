# В этом файле происходит запуск, и основной цикл while running
# Уже в нём вызываются функции из отдельных файлов в зависимости от того что сейчас происходит в игре

import pygame
from const import service, sizes
import start_menu


def main():
    pygame.init()
    screen = pygame.display.set_mode(sizes.WINDOW_SIZE)
    actions = {service.START_MENU: start_menu.run}
    cur_action = service.START_MENU
    while cur_action != service.QUIT:
        cur_action = actions[cur_action]()


main()
