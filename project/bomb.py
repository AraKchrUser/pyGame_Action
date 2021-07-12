import os
import sys
import pygame

pygame.init()
size = 500, 500
screen = pygame.display.set_mode(size)  # создаем холст


def load_image(name, colorkey=None):
    """"Загрузка изображения и конвертирование"""

    fullname = os.path.join(r'data', name)
    print(fullname)

    if not os.path.isfile(fullname):
        print('not found file')
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()

        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
        print('converted')

    return image


class Bomb(pygame.sprite.Sprite):
    """Класс для обработки столкновения и перемещения бомбы"""

    image = pygame.transform.scale(load_image(r'sprites\bomb.png'), (30, 30))

    def __init__(self, x, y, *group):

        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Флаг взрыва
        self.boom = False

        # Флаг перемещения
        self.moving = False

    def update(self, *args):

        # Обработка перемещения спрайта игнроком с помощью мыши
        if args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.moving = True
        if args[0].type == pygame.MOUSEMOTION and self.moving:
            self.rect.x, self.rect.y = args[0].pos
        if args[0].type == pygame.MOUSEBUTTONUP:
            self.moving = False

        # При столкновении со стрелой
        if pygame.sprite.spritecollide(self, args[1], True):
            self.boom = not self.boom
