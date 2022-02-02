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
