import pygame
from const import sizes, service, colors, file_paths
from tools import classes, methods, towers


class Lives(pygame.sprite.Sprite):
    pattern = methods.load_image(file_paths.LIVES_IMAGE)
    font = pygame.font.Font(None, sizes.RES_FONT_SIZE)

    def __init__(self, points, *args):
        super().__init__(*args)
        self.points = points
        self.start_points = points
        self.display_lives()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(sizes.LIVES_POS)

    def __iadd__(self, other):
        self.points += other
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
        self.money += other
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


class Panel:
    cell_size = 100
    border_size = 2
    width, height = size = 4, 2
    image_width, image_height = image_size = (cell_size + border_size) * width + border_size, \
                                             (cell_size + border_size) * height + border_size
    img_cords = 0, 0
    none_item = (None, lambda: 0, 0)
    sell_icon = methods.load_image(file_paths.SELL_ICON)
    upgrade_icon = methods.load_image(file_paths.UPGRADE_ICON)

    def __init__(self):
        self.cells = [[self.none_item] * self.height for _ in range(self.width)]

    def draw(self, screen):
        panel = pygame.Surface(self.image_size)
        panel.fill(colors.PANEL)
        cords = screen.get_width() - self.image_width, screen.get_height() - self.image_height
        self.img_cords = cords
        border_cell_size = self.cell_size + self.border_size
        for i in range(self.width + 1):
            pygame.draw.line(panel, colors.PANEL_BORDER, (border_cell_size * i, 0),
                             (border_cell_size * i, self.image_height), self.border_size)
        for i in range(self.height + 1):
            pygame.draw.line(panel, colors.PANEL_BORDER, (0, border_cell_size * i),
                             (self.image_width, border_cell_size * i), self.border_size)
        for i in range(self.width):
            for j in range(self.height):
                if not self.cells[i][j][0]:
                    continue
                panel.blit(self.cells[i][j][0],
                           (i * border_cell_size + self.border_size, j * border_cell_size + self.border_size))
        screen.blit(panel, cords)

    def set_item(self, i, j, img, func, price, cl=None):
        img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
        price_img = methods.get_price_img(price)
        price_x, price_y = self.cell_size - price_img.get_width(), self.cell_size - price_img.get_height()
        img.blit(price_img, (price_x, price_y))
        self.cells[i][j] = img, func, cl

    def on_click(self, cords):
        pos = self.get_pos(cords)
        if not pos:
            return
        self.get_click(pos)

    def get_pos(self, cords):
        cords = cords[0] - self.img_cords[0], cords[1] - self.img_cords[1]
        if cords[0] < 0 or cords[1] < 0:
            return None
        i = cords[0] // (self.cell_size + self.border_size)
        j = cords[1] // (self.cell_size + self.border_size)
        if i >= self.width or j >= self.height:
            return None
        return i, j

    def get_click(self, pos):
        item = self.cells[pos[0]][pos[1]]
        methods.build_tower(*item[1])
        self.clear()

    def clear(self):
        for i in range(self.width):
            for j in range(self.height):
                self.cells[i][j] = self.none_item

    def set_building(self, tower_place, towers_sprites, entities_sprites, all_sprites, money):
        self.clear()
        i, j = 0, 0
        for tow in towers.tower_classes:
            self.set_item(i, j, tow.icon,
                          (tow, tower_place, money, towers_sprites, entities_sprites, all_sprites), tow.price, tow)
            i += 1
            if i == self.width:
                i = 0
                j += 1

    def set_tower_panel(self, tower, money, *place_groups):
        self.set_item(0, 0, self.upgrade_icon, lambda: tower.upgrade(money), tower.upgrade_price)
        self.set_item(self.width - 1, self.height - 1, self.sell_icon, lambda: tower.sell(money, *place_groups),
                      int(tower.cost * 0.7))


