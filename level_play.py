import pygame
from const import service
from tools import classes, methods, towers, enemies
import csv

started = False
level = 0
all_sprites = pygame.sprite.Group()
tower_sprites = pygame.sprite.Group()
tower_places_sprites = pygame.sprite.Group()
twist_points = []
background = pygame.Surface((0, 0))
clock = pygame.time.Clock()


def run(screen,  *args, **kwargs):
    global all_sprites, level
    level = 1
    load_level()
    running = service.LEVEL_PLAY
    monster = enemies.Enemy(twist_points, all_sprites)
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
    all_sprites = pygame.sprite.Group()
    return running


def set_level(x):
    global level
    level = x


def load_level():
    global all_sprites, twist_points, tower_places_sprites, background
    background = classes.Background(f"levels_data/{level}level_background.png", all_sprites)
    try:
        fin = open(f"data/levels_data/{level}level.csv")
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
        print("Не удалось открыть файл data/levels_data/0level.csv", e)
