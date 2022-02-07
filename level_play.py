import pygame
from const import service, file_paths, sizes
from tools import classes, methods, towers, enemies, interface
import csv

in_progress = False
level = 0


def run(screen,  *args, **kwargs):
    global level, in_progress
    all_sprites = pygame.sprite.Group()
    entities_sprites = pygame.sprite.Group()
    towers_sprites = pygame.sprite.Group()
    enemies_sprites = pygame.sprite.Group()

    level = 0
    waves, tower_places_sprites, background, lives, pause_btn, money, panel = load_level(all_sprites, entities_sprites)
    current_wave = 0
    if not waves:
        return service.MAIN_MENU
    running = service.LEVEL_PLAY
    clock = pygame.time.Clock()
    while running == service.LEVEL_PLAY:
        tick = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = service.QUIT
                break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pause_btn.get_click(*event.pos):
                    running = pause(screen)
                    clock.tick()
                panel.on_click(event.pos)
        if current_wave < len(waves):
            result = waves[current_wave].summon(tick, all_sprites, enemies_sprites, entities_sprites)
            if result == Wave.LAST_ENEMY:
                current_wave += 1
        entities_sprites.update(tick, enemies_sprites, entities_sprites, all_sprites)
        for enemy in enemies_sprites:
            if enemy.hp <= 0:
                money += enemy.reward
                enemy.health_bar.kill()
                enemy.kill()
            if enemy.gone:
                lives -= enemy.price
                enemy.kill()
                if lives.get_points() == 0:
                    gameover()
                    running = service.QUIT()
                    break
        all_sprites.draw(screen)
        panel.draw(screen)
        pygame.display.flip()
    in_progress = False
    return running


def gameover():
    pass


def set_level(x):
    global level
    if not in_progress:
        level = x


def load_level(all_sprites, entities_sprites):
    try:
        global in_progress
        in_progress = True
        ways = []
        tower_places_sprites = pygame.sprite.Group()
        waves = []
        fin = open(file_paths.LEVEL_DATA.format(level))
        reader = csv.reader(fin, delimiter=";")

        bckg_file = reader.__next__()[0]
        background = classes.Background(bckg_file, all_sprites)
        lives = interface.Lives(int(reader.__next__()[0]), all_sprites)
        money = interface.Money(int(reader.__next__()[0]), all_sprites)
        pause_btn = classes.Button(file_paths.PAUSE_BUTTON, *sizes.PAUSE_POS, all_sprites)
        panel = interface.Panel()

        cnt_places = int(reader.__next__()[0])
        for _ in range(cnt_places):
            coords = reader.__next__()
            place = towers.TowerPlace((int(coords[0]), int(coords[1])), all_sprites, tower_places_sprites)
            if _ == 0:
                x = place.rect.centerx
                y = place.rect.bottom
                place.kill()
                towers.Tower(x, y, all_sprites, entities_sprites)
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
        print("Не удалось открыть файл " + file_paths.LEVEL_DATA.format(level), e)
        return None, None, None, None, None, None
    return waves, tower_places_sprites, background, lives, pause_btn, money, panel


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


def pause(screen):
    buttons = pygame.sprite.Group()
    menu = methods.load_image(file_paths.LAUNCH_BACKGROUND)
    menu_width, menu_height = menu.get_size()
    running = service.PAUSE
    menux = (sizes.WINDOW_WIDTH - menu_width) / 2
    menuy = (sizes.WINDOW_HEIGHT - menu_height) / 2
    continue_btn = classes.Button(file_paths.CONTINUE_BTN, 0, (menu_height - 75 * 2) / 3, buttons)
    continue_btn.rect.centerx = menu_width / 2
    exit_btn = classes.Button(file_paths.EXIT_LEVEL_BTN, 9, (menu_height - 75 * 2) / 3 * 2 + 75, buttons)
    exit_btn.rect.centerx = menu_width / 2

    buttons.draw(menu)

    screen.blit(menu, (menux, menuy))
    pygame.display.flip()
    while running == service.PAUSE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = service.QUIT
                break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = event.pos[0] - menux
                y = event.pos[1] - menuy
                if continue_btn.get_click(x, y):
                    running = service.LEVEL_PLAY
                if exit_btn.get_click(x, y):
                    running = service.MAIN_MENU
    return running
