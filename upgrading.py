import pygame
from const import service
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from const.file_paths import UPGRADING_BACKGROUND, CLOSE_BUTTON
from tools.methods import load_image
from tools.classes import Button


def run(screen,  *args, **kwargs):
    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()
    upgrading_button = pygame.sprite.Group()

    background = pygame.transform.scale(load_image('Frame 1 (1).png'), (WINDOW_WIDTH, 1719))
    close_button = Button(CLOSE_BUTTON, all_sprites, button_sprites, 1490, 20)


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
                    up_coord = max(-919, up_coord - 50)
                if close_button.get_click(event.pos[0], event.pos[1]):
                    return service.MAIN_MENU

        screen.blit(background, (0, up_coord))
        button_sprites.draw(screen)
        pygame.display.flip()

