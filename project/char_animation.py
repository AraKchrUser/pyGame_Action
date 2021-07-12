import pygame
from bullet import Bullet


class AnimationSprites(pygame.sprite.Sprite):
    """Анимация спрайтов с персонажами"""

    def __init__(self, sheet, columns, rows, x, y, reverse, ranger, *group):
        super().__init__(group[0])

        #  Инициализация кадров состояния игрока в течение игры
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.reverse = reverse

        self.stop = None    # Длина анимации
        self.stopping = False    # Остановка анимации
        self.speed = 5    # Скорость анимации
        self.dead = False    # Индикатор смерти персонажа
        self.ranger = ranger    # Персонаж - стрелок
        if self.ranger:
            self.group_bullet = group[1]

    def cut_sheet(self, sheet, columns, rows):
        """Определить кадры состояния персонажа"""

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, *args):

        self.stop = args[2]

        # При столкновении с бомбой
        bombs = pygame.sprite.spritecollide(self, args[0], False)
        for bomb in bombs:
            bomb.boom = not bomb.boom

        # При столкновении со стрелой
        if pygame.sprite.spritecollide(self, args[1], True):
            self.stopping = True
            self.cur_frame = 0
        if bombs:
            self.stopping = not self.stopping
            self.cur_frame = 0

        # Проиграть анимацию
        if not self.stopping:
            frame = self.frames[:-self.stop]
            self.cur_frame = (self.cur_frame + 1) % (len(self.frames[:-self.stop]))
            if 20 < self.cur_frame < 31:
                self.rect.x -= self.speed

            if self.ranger:
                if self.cur_frame == 36:
                    Bullet(self, self.group_bullet)
        else:
            frame = self.frames[-self.stop:]
            self.cur_frame = (self.cur_frame + 1) % (len(frame))
            if self.cur_frame == self.stop - 1:
                self.dead = not self.dead

        if self.reverse:
            self.image = pygame.transform.flip(frame[self.cur_frame], True, False)
        else:
            self.image = frame[self.cur_frame]
