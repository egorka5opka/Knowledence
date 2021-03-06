# файл с методами которые много где понадобятся
import os
import csv
import pygame
import math
from const import file_paths, sizes, colors
from const.service import *


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        fullname = os.path.join('data', file_paths.NO_IMAGE)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def load_enemy(enemy_file, return_type=0):
    for_exception = (load_image("enemies/monster.png"), 100, 60, False, 1, 8)
    try:
        fin = open(enemy_file)
        reader = csv.DictReader(fin, delimiter=";")
        enemy = reader.__next__()
        fin.close()
        if return_type:
            frames1 = cut_sheet(load_image(enemy[IMAGE_PATH]), int(enemy["columns"]), int(enemy["rows"]))
            frames = [frames1, [pygame.transform.flip(f, True, False) for f in frames1.copy()]]
            return [frames, int(enemy[HEALTH]), int(enemy[VELOCITY]),
                    enemy[FLYING] == "1", int(enemy[PRICE]), int(enemy[REWARD])]
        return enemy
    except FileNotFoundError:
        print(f"File not found {enemy_file}")
        return for_exception
    except ValueError:
        print(f"Incorrect file data {enemy_file}")
        return for_exception
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return for_exception


def load_tower(tower_file, return_type=0,):
    try:
        fin = open(tower_file)
        reader = csv.DictReader(fin, delimiter=";")
        tower = reader.__next__()
        fin.close()
        frames = cut_sheet(load_image(tower[IMAGE_PATH]), int(tower["columns"]), int(tower["rows"]))
        if return_type:
            time = -1
            if BULLET_TIME in tower:
                time = float(tower[BULLET_TIME])
                print(time)
            return [frames, int(tower[DAMAGE]), int(tower[PRICE]), float(tower[ATTACK_SPEED]), tower[ATTACK_AIR] == "1",
                    float(tower[TOWER_DAMAGE_BUFF]), float(tower[TOWER_VELOCITY_BUFF]), float(tower[TOWER_BUFFS_TIME])
                    * 1000, load_image(tower[BULLET_IMAGE]), int(tower[BULLET_VELOCITY]), int(tower[ATTACK_RADIUS]),
                    load_image(tower[TOWER_ICON]), time * 1000]
        return tower
    except FileNotFoundError:
        print(f"File not found {tower_file}")
        return
    except ValueError as e:
        print(f"Incorrect file data {tower_file}, {e}")
        return
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return


def cut_sheet(sheet, columns, rows):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
    frames = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames


def tower_dist(x, y, b):
    dx = x - b.centerx
    dy = y - b.centery
    return dx * dx + dy * dy


def radians_to_degrees(rad):
    return rad / math.pi * 180


def build_tower(tower_class, tower_place, money, *groups):
    if money.get_money() < tower_class.price:
        return
    x = tower_place.rect.centerx
    y = tower_place.rect.bottom
    tower_class(x, y, *groups)
    tower_place.kill()
    money -= tower_class.price


def get_price_img(n):
    size = sizes.price_size
    font = pygame.font.Font(None, size[1] + 10)
    text = font.render(str(n), True, colors.TEXT)
    return text
