import pygame
from tools.methods import load_image
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

    waves, tower_places_sprites, background, lives, pause_btn, money, panel = load_level(all_sprites, entities_sprites)
    current_wave = 0
    if not waves:
        return service.MAIN_MENU
    running = service.LEVEL_PLAY
    clock = pygame.time.Clock()
    was_victory = False
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
                if was_victory:
                    continue
                panel.on_click(event.pos)
                for place in tower_places_sprites:
                    place.click(event.pos,
                                lambda p: panel.set_building(p, towers_sprites, entities_sprites, all_sprites, money))
                for tower in towers_sprites:
                    tower.click(event.pos, lambda t: panel.set_tower_panel(t, money, tower_places_sprites,
                                                                           entities_sprites, all_sprites))
        if current_wave < len(waves):
            result = waves[current_wave].summon(tick, all_sprites, enemies_sprites, entities_sprites)
            if result == Wave.LAST_ENEMY:
                current_wave += 1
        elif not len(enemies_sprites) and not was_victory:
            running = victory(screen, lives)
            was_victory = True
            continue
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
                    gameover(screen)
                    running = service.QUIT()
                    break
        all_sprites.draw(screen)
        panel.draw(screen)
        pygame.display.flip()
    in_progress = False
    return running


def gameover(screen):
    SELF_WIDTH, SELF_HEIGHT = 742, 447
    all_sprites = pygame.sprite.Group()
    background = pygame.transform.scale(load_image(file_paths.LAUNCH_BACKGROUND), (SELF_WIDTH, SELF_HEIGHT))
    classes.Button(file_paths.DEFEAT_LABEL, 641, 295, all_sprites)

    classes.Button(file_paths.EMPTY_STAR, 646, 207, all_sprites)
    classes.Button(file_paths.EMPTY_STAR, 735, 194, all_sprites)
    classes.Button(file_paths.EMPTY_STAR, 824, 207, all_sprites)

    go_main = classes.Button(file_paths.EXIT_LEVEL_BTN, 566, 405, all_sprites)
    show_butt = classes.Button(file_paths.SHOW_LEVEL, 566, 505, all_sprites)
    screen.blit(background, ((sizes.WINDOW_WIDTH - SELF_WIDTH) // 2, (sizes.WINDOW_HEIGHT - SELF_HEIGHT) // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return service.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if go_main.get_click(event.pos[0], event.pos[1]):
                    return service.MAIN_MENU
                elif show_butt.get_click(event.pos[0], event.pos[1]):
                    return service.LEVEL_PLAY
        all_sprites.draw(screen)
        pygame.display.flip()


def victory(screen, lives):
    global level

    reading = open("data/progress.txt", mode='r')
    count = int(reading.readline())
    levels_progress = reading.readline().split(',')
    upgrading_count = int(reading.readline())

    SELF_WIDTH, SELF_HEIGHT = 742, 447
    all_sprites = pygame.sprite.Group()
    background = pygame.transform.scale(load_image(file_paths.LAUNCH_BACKGROUND), (SELF_WIDTH, SELF_HEIGHT))
    classes.Button(file_paths.WIN_LABEL, 641, 295, all_sprites)

    now_stars = 1
    classes.Button(file_paths.FILLED_STAR, 646, 207, all_sprites)
    if lives.start_points * 0.4 <= lives.get_points():
        classes.Button(file_paths.FILLED_STAR, 735, 194, all_sprites)
        now_stars += 1
    else:
        classes.Button(file_paths.EMPTY_STAR, 735, 194, all_sprites)
    if lives.start_points * 0.7 <= lives.get_points():
        classes.Button(file_paths.FILLED_STAR, 824, 207, all_sprites)
        now_stars += 1
    else:
        classes.Button(file_paths.EMPTY_STAR, 824, 207, all_sprites)

    if levels_progress[level] == '0':
        levels_progress[level] = str(now_stars)
        count += 1
        upgrading_count += now_stars
        reading.close()
        reading = open("data/progress.txt", mode='w')
        reading.write(str(count) + '\n' + ','.join(levels_progress) + str(upgrading_count))
    elif int(levels_progress[level]) < now_stars:
        levels_progress[level] = str(now_stars)
        upgrading_count += now_stars - int(levels_progress[level])
        reading.close()
        reading = open("data/progress.txt", mode='w')
        reading.write(str(count) + '\n' + ','.join(levels_progress) + str(upgrading_count))

    go_main = classes.Button(file_paths.EXIT_LEVEL_BTN, 566, 405, all_sprites)
    show_butt = classes.Button(file_paths.SHOW_LEVEL, 566, 505, all_sprites)
    screen.blit(background, ((sizes.WINDOW_WIDTH - SELF_WIDTH) // 2, (sizes.WINDOW_HEIGHT - SELF_HEIGHT) // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return service.QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if go_main.get_click(event.pos[0], event.pos[1]):
                    return service.MAIN_MENU
                elif show_butt.get_click(event.pos[0], event.pos[1]):
                    return service.LEVEL_PLAY
        all_sprites.draw(screen)
        pygame.display.flip()


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
        print("???? ?????????????? ?????????????? ???????? " + file_paths.LEVEL_DATA.format(level), e)
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
                enemy_class, cnt, way = self.enemies[-1]
                e = enemy_class(way, *sprite_groups)
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
