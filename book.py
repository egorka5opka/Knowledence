import pygame
from const import service
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from const.file_paths import BOOK_BACKGROUND, CLOSE_BUTTON, UPGRADE_BUTTON
from tools.methods import load_image
from tools.classes import Button
import csv
from const.service import UPGR_BUTT_ORDER
import tools.interface


def run(screen, *args, **kwargs):
    all_sprites = pygame.sprite.Group()

    background = load_image(BOOK_BACKGROUND)
    close_button = Button(CLOSE_BUTTON, 1490, 20, all_sprites)
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
                elif event.button == 5:
                    up_coord = max(-350, up_coord - 50)
                elif close_button.get_click(event.pos[0], event.pos[1]):
                    return service.MAIN_MENU
        screen.blit(background, (0, up_coord))
        all_sprites.draw(screen)
        pygame.display.flip()
