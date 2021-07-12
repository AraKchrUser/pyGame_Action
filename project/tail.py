import bomb
import pygame
import os


tile_images = {'tail1': bomb.load_image(r'tile\tail4.png'),
               'tail2': bomb.load_image(r'tile\tail2.png'),
               'tail3': bomb.load_image(r'tile\tail3.png')}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    """Инициализация тайлов"""

    def __init__(self, tile_type, pos_x, pos_y, tiles_group):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


def load_level(filename):
    """Функция загрузки карты уровня"""

    fullname = os.path.join(r'data', filename)

    with open(fullname, 'r') as mapf:
        level = [line.strip() for line in mapf]

    #  Заполнение карты до прямоугольника
    width = max(map(len, level))
    return list(map(lambda x: x.ljust(width, '.'), level))
