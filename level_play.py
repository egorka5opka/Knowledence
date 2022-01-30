import pygame
from const import service, file_paths
from tools import classes, methods, towers, enemies
import csv

started = False
level = 0


def run(screen,  *args, **kwargs):
    global level
    all_sprites = pygame.sprite.Group()
    entities_sprites = pygame.sprite.Group()
    towers_sprites = pygame.sprite.Group()
    enemies_sprites = pygame.sprite.Group()

    level = 0
    waves, tower_places_sprites, background = load_level(all_sprites)
    current_wave = 0
    if not waves:
        return service.MAIN_MENU
    running = service.LEVEL_PLAY
    clock = pygame.time.Clock()
    while running == service.LEVEL_PLAY:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = service.QUIT
                break
        tick = clock.tick()
        if current_wave < len(waves):
            result = waves[current_wave].summon(tick, all_sprites, enemies_sprites, entities_sprites)
            if result == Wave.LAST_ENEMY:
                current_wave += 1
        entities_sprites.update(tick)
        all_sprites.draw(screen)
        pygame.display.flip()
    return running


def set_level(x):
    global level
    level = x


def load_level(all_sprites):
    try:
        ways = []
        tower_places_sprites = pygame.sprite.Group()
        waves = []
        fin = open(file_paths.LEVEL_DATA.format(level))
        reader = csv.reader(fin, delimiter=";")
        bckg_file = reader.__next__()[0]
        background = classes.Background(bckg_file, all_sprites)
        cnt_places = int(reader.__next__()[0])
        for _ in range(cnt_places):
            coords = reader.__next__()
            towers.TowerPlace((int(coords[0]), int(coords[1])), all_sprites, tower_places_sprites)
        cnt_ways = int(reader.__next__()[0])
        for _ in range(cnt_ways):
            twist_points = []
            cnt_points = int(reader.__next__()[0])
            for __ in range(cnt_points):
                coords = reader.__next__()
                twist_points.append((int(coords[0]), int(coords[1])))
            ways.append(tuple(twist_points))
        cnt_waves = int(reader.__next__()[0])
        for _ in range(cnt_waves):
            waves.append(Wave(reader, ways))
        fin.close()
    except Exception as e:
        print("Не удалось открыть файл data/" + file_paths.LEVEL_DATA.format(level), e)
        return None, None, None
    return waves, tower_places_sprites, background


class Wave:
    SUMMON_ENEMY = 1
    NOT_SUMMON_ENEMY = 0
    LAST_ENEMY = -1

    def __init__(self, reader, ways):
        self.size, self.time = map(int, reader.__next__())
        self.enemies = []
        self.delay_time = 1000.0
        self.delay = 0
        for _ in range(self.size):
            name, cnt, way = reader.__next__()
            self.enemies.append([enemies.get_enemy_class(name), int(cnt), ways[int(way) - 1]])
        self.enemies.reverse()

    def summon(self, tick, *sprite_groups):
        if self.time > 0:
            self.time -= tick
            return self.NOT_SUMMON_ENEMY
        else:
            if self.delay > 0:
                self.delay -= tick
                return self.NOT_SUMMON_ENEMY
            else:
                self.delay = self.delay_time
                name, cnt, way = self.enemies[-1]
                enemies.get_enemy_class(name)(way, *sprite_groups)
                self.enemies[-1][1] -= 1
                if self.enemies[-1][1] == 0:
                    self.enemies = self.enemies[:-1]
                    if not self.enemies:
                        return self.LAST_ENEMY
                return self.SUMMON_ENEMY
