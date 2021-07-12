import pygame
from bullet import Bullet


class BloodRanger(pygame.sprite.Sprite):
    """Класс для управления лучником"""

    def __init__(self, sheet, columns, rows, x, y, reverse, *group):
        super().__init__(*group)

        #  Инициализировать фреймы состояний
        self.frames_stand = []
        self.frames_moving = []
        self.frames_dead = []
        self.frames_attack = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames_stand[self.cur_frame]
        self.rect = self.rect.move(x, y)

        #  Порядок действий и скорость персонажа
        self.reverse = reverse
        self.speed = 5

        #  Индикаторы состояний
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False
        self.attack = False
        self.attack_count = 0
        self.dead = False
        self.stopping = False

    def cut_sheet(self, sheet, columns, rows):
        """Определить состояния персонажа для дальнейшей анимации"""

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                if j == 0 or j == 1:
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames_stand.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                if j == 2:
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames_moving.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                if j == 3:
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames_attack.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                if j == 4:
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames_dead.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def change_state(self, frames_list, *args):
        """Изменить состояние"""

        self.cur_frame = (self.cur_frame + 1) % (len(frames_list))
        self.image = frames_list[self.cur_frame]

    def attack_stop(self):
        """Остановить нападение персонажа"""
        self.attack = False
        self.attack_count = 0

    def update(self, *args):

        #  Пока персонаж не 'умер', обрабатываем события, связанные с ним
        if not self.dead:
            if self.moving_right:
                self.attack_stop()
                self.rect.centerx += self.speed
                self.change_state(self.frames_moving, *args)
            if self.moving_left:
                self.attack_stop()
                self.rect.centerx -= self.speed
                self.change_state(self.frames_moving, *args)
            if self.moving_top:
                self.attack_stop()
                self.rect.centery -= self.speed
                self.change_state(self.frames_moving, *args)
            if self.moving_bottom:
                self.attack_stop()
                self.rect.centery += self.speed
                self.change_state(self.frames_moving, *args)
            if not self.moving_bottom and not self.moving_top and not self.moving_right and not self.moving_left:
                self.change_state(self.frames_stand, *args)
            if self.attack:
                if not self.attack_count:
                    self.cur_frame = 0
                self.attack_count += 1
                self.change_state(self.frames_attack, *args)
                if not ((self.cur_frame + 1) % len(self.frames_attack)):
                    Bullet(self, args[0])

            #  Персонаж погибает
            if pygame.sprite.spritecollideany(self, args[1]):
                self.dead = not self.dead
                self.cur_frame = 0
            if pygame.sprite.spritecollide(self, args[2], True):
                self.dead = not self.dead
                self.cur_frame = 0

        elif not self.stopping:
            #  Анимация смерти персонажа
            self.change_state(self.frames_dead, *args)
            if self.cur_frame == len(self.frames_dead) - 1:
                self.stopping = True

        if self.stopping:
            #  Персонаж погибает
            self.image = self.frames_dead[-1]
