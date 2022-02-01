import pygame
from const import sizes, service, colors, file_paths
from tools import classes, methods


class Lives(pygame.sprite.Sprite):
    pattern = methods.load_image(file_paths.LIVES_IMAGE)
    font = pygame.font.Font(None, sizes.RES_FONT_SIZE)

    def __init__(self, points, *args):
        super().__init__(*args)
        self.points = points
        self.display_lives()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(sizes.LIVES_POS)

    def __iadd__(self, other):
        self.points -= other
        self.display_lives()
        return self

    def __isub__(self, other):
        self.points -= other
        self.display_lives()
        return self

    def get_points(self):
        return self.points

    def display_lives(self):
        self.image = self.pattern.copy()
        text = self.font.render(str(self.points), True, colors.MAIN_TEXT_COLOR)
        self.image.blit(text, (65, 12))


class Money(pygame.sprite.Sprite):
    pattern = methods.load_image(file_paths.MONEY_IMAGE)
    font = pygame.font.Font(None, sizes.RES_FONT_SIZE)

    def __init__(self, money, *args):
        super().__init__(*args)
        self.money = money
        self.display_money()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(sizes.MONEY_POS)

    def __iadd__(self, other):
        self.money -= other
        self.display_money()
        return self

    def __isub__(self, other):
        self.money -= other
        self.display_money()
        return self

    def get_money(self):
        return self.money

    def display_money(self):
        self.image = self.pattern.copy()
        text = self.font.render(str(self.money), True, colors.MAIN_TEXT_COLOR)
        self.image.blit(text, (70, 12))


class PauseButton(pygame.sprite.Sprite):
    image_btn = methods.load_image(file_paths.PAUSE_BUTTON)

    def __init__(self, *args):
        super().__init__(*args)
        self.image = self.image_btn
        self.rect = self.image.get_rect().move(sizes.PAUSE_POS)

    def clicked(self, pos):
        cursor = classes.SupportCursor(*pos)
        res = bool(pygame.sprite.collide_rect(cursor, self))
        cursor.kill()
        return res
