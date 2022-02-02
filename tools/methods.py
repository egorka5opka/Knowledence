# файл с методами которые много где понадобятся
import os
import csv
import pygame
import math
from const import file_paths
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
            return [load_image(enemy[IMAGE_PATH]), int(enemy[HEALTH]), int(enemy[VELOCITY]),
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
            return [frames, int(tower[DAMAGE]), int(tower[PRICE]), int(tower[ATTACK_SPEED]),
                    tower[ATTACK_AIR] == "1", int(tower[TOWER_DAMAGE_BUFF]), int(tower[TOWER_VELOCITY_BUFF]),
                    load_image(tower[BULLET_IMAGE]), tower[BULLET_VELOCITY]]
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
    print(rect.size, rows, columns)
    frames = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, rect.size)))
    return frames
