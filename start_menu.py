import pygame
from const import service, sizes
from const.sizes import WINDOW_WIDTH, WINDOW_HEIGHT
from tools.methods import *
from tools.classes import Button


def run(screen):
    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()

    fon = pygame.transform.scale(load_image('start_fon.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    button = Button("Start_button.png", all_sprites, button_sprites, 658, 646)
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return service.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.get_click(event.pos[0], event.pos[1]):
                    return service.MAIN_MENU
        pygame.display.flip()
    return service.START_MENU
