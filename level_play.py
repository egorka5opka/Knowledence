import pygame
from const import service, file_paths
from tools import classes, methods, towers, enemies
import csv

started = False
level = 0


def run(screen,  *args, **kwargs):
    global level
    all_sprites = pygame.sprite.Group()
    tower_sprites = pygame.sprite.Group()
    level = 0
    twist_points, tower_places_sprites, background = load_level(all_sprites)
    if twist_points == None:
        return service.MAIN_MENU
    running = service.LEVEL_PLAY
    monster = enemies.Enemy(twist_points, all_sprites)
    clock = pygame.time.Clock()
    while running == service.LEVEL_PLAY:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = service.QUIT
                break
        monster.update(clock.tick())
        all_sprites.draw(screen)
        for i in range(len(twist_points) - 1):
            pygame.draw.line(screen, (0, 0, 0), twist_points[i], twist_points[i + 1], 5)
        pygame.display.flip()
    return running


def set_level(x):
    global level
    level = x


def load_level(all_sprites):
    background = classes.Background(file_paths.LEVEL_BACKGROUND.format(level), all_sprites)
    twist_points = []
    tower_places_sprites = pygame.sprite.Group()
    try:
        fin = open(file_paths.LEVEL_DATA.format(level))
        reader = csv.reader(fin, delimiter=";")
        cnt_points = int(reader.__next__()[0])
        for _ in range(cnt_points):
            coords = reader.__next__()
            twist_points.append((int(coords[0]), int(coords[1])))
        cnt_places = int(reader.__next__()[0])
        for _ in range(cnt_places):
            coords = reader.__next__()
            towers.TowerPlace((int(coords[0]), int(coords[1])), all_sprites, tower_places_sprites)
    except Exception as e:
        print("Не удалось открыть файл data/" + file_paths.LEVEL_DATA.format(level), e)
        return None, None, None
    return twist_points, tower_places_sprites, background
