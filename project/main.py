import random
import pygame
import sys
import bomb as bb
from bomb import load_image
from sample_animation_sprite import SpriteAnim
from tail import Tile, load_level
from blood_ranger import BloodRanger
from settings import *
from bullet import Bullet
from char_animation import AnimationSprites


pygame.init()
pygame.display.set_caption('')
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)  # создаем холст
start = True
horizontal_borders = pygame.sprite.Group()  # Горизонтальная граница
vertical_borders = pygame.sprite.Group()  # Вертикальная граница
border_image = pygame.sprite.Group()


class Health:
    """Класс для слежения за здоровьем персонажа"""

    def __init__(self):
        self.score = 100

    def render(self, dead_count):
        """Отобразить уровень здоровья и количество поверженных врагов"""

        font = pygame.font.Font(None, 20)
        text = font.render(f'Health {self.score}', 3, (255, 255, 255))
        screen.blit(text, (20, 20))
        text = font.render(f'Dead {dead_count}', 3, (255, 255, 255))
        screen.blit(text, (20, 35))


class Border(pygame.sprite.Sprite):
    """Класс для определения границ экрана"""

    def __init__(self, x1, y1, x2, y2):
        super().__init__(border_image)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def update(self, *args):
        if args:
            #  Пересечение стрелы с границей
            pygame.sprite.spritecollide(self, args[0], True)
            pygame.sprite.spritecollide(self, args[1], True)

            #  Пересечение персонажа-противника с границей
            if pygame.sprite.spritecollide(self, args[2], True):
                health.score -= 15


class Start:
    """Заставка игры и обработка нажатия на кнопку 'начать игру'"""

    def __init__(self):
        self.x, self.y, self.w, self.h = 0, 0, 0, 0

    def render(self, text_x, text_y, text_w, text_h):
        font = pygame.font.Font(None, 30)
        text = font.render('Start game', 1, (0, 0, 0))
        self.x = text_x - 10 + (text_w + 20 - text.get_width()) // 2
        self.y = text_y - 10 + text_h + 25
        self.w = text.get_width()
        self.h = text.get_height()
        pygame.draw.rect(screen, (50, 50, 50), (self.x + 3, self.y + 3, self.w, self.h), 0)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 0)
        screen.blit(text, (self.x + (self.w - text.get_width()) // 2, self.y + (self.h - text.get_height()) // 2))

    def click(self, position):
        if self.x <= position[0] <= self.x + self.w and self.y <= position[1] <= self.y + self.h:
            return 1
        return 0


def terminate():
    """Выход из игры"""

    pygame.quit()
    sys.exit()


def start_data_render():
    """Определить фон заставки"""

    c = ['black', 'red', 'yellow', 'blue']
    screen.fill((200, 200, 200))
    for i in range(1000):
        screen.fill(pygame.Color(c[i % len(c)]), (random.random() * WIDTH, random.random() * HEIGHT, 1, 1))

    font = pygame.font.SysFont('Arial', 50, bold=True, italic=True)

    color = pygame.Color(0, 250, 0)
    hsv = color.hsva
    color.hsva = hsv[0], hsv[1], hsv[2] - 50, hsv[3]
    text = font.render("Hello, Pygame!", True, color)
    hsv = color.hsva
    color.hsva = hsv[0], hsv[1], hsv[2] + 40, hsv[3]
    text2 = font.render("Hello, Pygame!", True, color)

    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()

    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (text_x + 3, text_y))

    pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 5)

    start_button.render(text_x, text_y, text_w, text_h)


if __name__ == '__main__':

    running = True
    fps = 60
    clock = pygame.time.Clock()
    dead_count = 0

    start_button = Start()

    #  Опредилить спрайтовые группы для игровых объектов
    bomb_sprites = pygame.sprite.Group()
    blood_ranger_sprites = pygame.sprite.Group()  # Заносим кровавого ренджера в отдельную группу
    hero_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    health_group = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    boom_sprites = pygame.sprite.Group()
    bullets_dark_range = pygame.sprite.Group()

    # Генерация тайлов
    level = load_level(r'maps\map')
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('tail1', x, y, tiles_group)
            elif level[y][x] == '#':
                Tile('tail2', x, y, tiles_group)
            elif level[y][x] == '@':
                Tile('tail3', x, y, tiles_group)

    #  Определить границы
    Border(5, 5, WIDTH - 5, 5)
    Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

    #  Генерация начальных объектов
    for i in range(5):
        bb.Bomb(300, 100 + i * 30, bomb_sprites)
    for i in range(2):
        SpriteAnim(pygame.transform.scale(load_image(r'sprites\HealthPickup.png', colorkey=-1),
                                          (250, 50)), 4, 1, random.randrange(50, WIDTH - 50),
                   random.randrange(50, HEIGHT - 50), False, health_group)

    health = Health()

    position = [50, 200, 350]   # Позиции персонажей-противников в поле

    #  Генерация начальных спрайтов
    AnimationSprites(pygame.transform.scale(load_image(r'sprites\DarkRanger.png'),
                                             (500, 300)), 10, 5, 395, 50, True, True, hero_sprites, bullets_dark_range)
    blood_ranger = BloodRanger(pygame.transform.scale(load_image(r'sprites\BloodRanger.png'),
                                                  (500, 300)), 10, 5, 100, HEIGHT // 2, False, blood_ranger_sprites)
    AnimationSprites(pygame.transform.scale(load_image(r'sprites\GreyMinotaur.png'),
                                              (900, 700)), 10, 5, 400, 350, True, False, hero_sprites)
    AnimationSprites(pygame.transform.scale(load_image(r'sprites\RedOrc.png'),
                                               (500, 300)), 10, 5, 405, 200, True, False, hero_sprites)

    #  Загрузка звука взрыва
    sounds_boom = pygame.mixer.Sound(r'data\sound\boom4.wav')

    set_timer = 0

    #  Загрузка музыки
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.music.load(r'data\sound\Campaign.ogg')
    pygame.mixer.music.play(-1, 0.0)

    # Игровой цикл
    while running:

        pause = False

        if start:
            start_data_render()
            pygame.draw.circle(screen, (0, 0, 255), pygame.mouse.get_pos(), 5)
            pygame.mixer.music.pause()
        else:
            if not set_timer:
                # Создание обработчиков
                delay = 250  # условное значение
                pygame.time.set_timer(ANIM, delay)
                pygame.time.set_timer(BOMB, delay * 600)  # Каждые 2.5 минут
                pygame.time.set_timer(HLTH, delay * 1200)  # Каждые 5 минут
                pygame.time.set_timer(MNOT, delay * 100)
                pygame.time.set_timer(RNGR, delay * 120)
                set_timer += 1

            screen.fill(pygame.Color('white'))
            tiles_group.draw(screen)  # Отрисовка тайлов
            health.render(dead_count)

            #  Стрельба из лука
            for bullet in bullets.sprites():
                bullet.draw(screen)
            bullets.update()
            for bullet in bullets_dark_range.sprites():
                bullet.draw(screen)
            bullets_dark_range.update(origin='-')

            # Отрисовка границ и персечение вертикальной границы с персонажем
            border_image.draw(screen)
            border_image.update()
            vertical_borders.update(bullets, bullets_dark_range, hero_sprites)

            bomb_sprites.draw(screen)
            bomb_sprites.update(event, bullets, hero_sprites)
            for bomb in bomb_sprites:
                #  Удаляем бомбу и подставляем взрыв
                if bomb.boom:
                    boom_anim = SpriteAnim(pygame.transform.scale(load_image(r'sprites\bomm.png', colorkey=-1),
                                                                  (400, 400)), 6, 6, bomb.rect.x,
                                           bomb.rect.y, False, boom_sprites)
                    sounds_boom.play()
                    bomb_sprites.remove(bomb)

            boom_sprites.draw(screen)
            for boom in boom_sprites:
                if boom.stopping:
                    boom_sprites.remove(boom)

            hero_sprites.draw(screen)
            # Удаление погибших персонажей
            for hero in hero_sprites:
                if hero.dead:
                    hero_sprites.remove(hero)
                    dead_count += 1

            blood_ranger_sprites.draw(screen)
            # Стрелок погиб
            for ranger in blood_ranger_sprites:
                if ranger.stopping:
                    health.score = 0

            # Стрелок получает здоровье (здоровье не превышает 100)
            if pygame.sprite.spritecollide(blood_ranger, health_group, True):
                if health.score + 15 > 100:
                    health.score = 100
                else:
                    health.score += 15

            health_group.draw(screen)

            # Музыка стоит на паузе
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.unpause()

        # Блок обработки событий
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Выход из игры
                terminate()

            if event.type == pygame.KEYDOWN:  # Обработка нажатий клавиш
                if event.key == pygame.K_p and not start:  # Пауза
                    pygame.mixer.music.pause()
                    pause = True

                # Перемещение лучника
                if event.key == pygame.K_RIGHT:
                    blood_ranger.moving_right = True
                elif event.key == pygame.K_LEFT:
                    blood_ranger.moving_left = True
                elif event.key == pygame.K_UP:
                    blood_ranger.moving_top = True
                elif event.key == pygame.K_DOWN:
                    blood_ranger.moving_bottom = True

                if event.key == pygame.K_SPACE:  # Атака
                    blood_ranger.attack = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    blood_ranger.moving_right = False
                elif event.key == pygame.K_LEFT:
                    blood_ranger.moving_left = False
                elif event.key == pygame.K_UP:
                    blood_ranger.moving_top = False
                elif event.key == pygame.K_DOWN:
                    blood_ranger.moving_bottom = False

            # Обработка пользовательских событий
            if event.type == ANIM:
                # Анимация объектов
                if not start:
                    hero_sprites.update(bomb_sprites, bullets, 10)
                    blood_ranger_sprites.update(bullets, hero_sprites, bullets_dark_range)
                    boom_sprites.update(35)
                    health_group.update()
            if event.type == BOMB:
                if not start:
                    # Отрисовка бомб
                    for i in range(5):
                        bb.Bomb(300, 100 + i * 30, bomb_sprites)
            if event.type == HLTH:
                if not start:
                    # Спрайты для повышения здоровья
                    for i in range(2):
                        SpriteAnim(pygame.transform.scale(load_image(r'sprites\HealthPickup.png', colorkey=-1),
                                                          (250, 50)), 4, 1, random.randrange(50, WIDTH - 50),
                                   random.randrange(50, HEIGHT - 50), False, health_group)
            # Генерация персонажей-противников
            if event.type == MNOT:
                if not start:
                    random.shuffle(position)
                    AnimationSprites(pygame.transform.scale(load_image(r'sprites\DarkRanger.png'),
                                                            (500, 300)), 10, 5, 395, position[0], True, True,
                                     hero_sprites, bullets_dark_range)
                    AnimationSprites(pygame.transform.scale(load_image(r'sprites\GreyMinotaur.png'),
                                                            (900, 700)), 10, 5, 400, position[1], True, False,
                                     hero_sprites)
                    AnimationSprites(pygame.transform.scale(load_image(r'sprites\RedOrc.png'),
                                                            (500, 300)), 10, 5, 405, position[2], True, False,
                                     hero_sprites)

            # Нажатие на кнопку инициализации игры
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start and start_button.click(event.pos):
                    start = not start
                    pygame.time.delay(1000)

        # Здоровья не осталось
        if health.score == 0:
            pygame.mixer.music.pause()
            font = pygame.font.Font(None, 60)
            text = font.render(f'GAME OVER', 30, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - 125, HEIGHT // 2))
            font = pygame.font.Font(None, 40)
            text = font.render(f'click P for exit', 20, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
            pause = True
            running = False

            with open(r'data\record\record.txt', 'r') as file:
                last_record = int(file.read())

            if last_record < dead_count:
                text = font.render(f'NEW RECORD!', 25, (255, 255, 255))  # New record
                screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))
                with open(r'data\record\record.txt', 'w') as file:
                    file.write(str(dead_count))
            else:
                text = font.render(f'LAST RECORD: {last_record}', 25, (255, 255, 255))  # Last record
                screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 + 100))

        pygame.display.flip()
        clock.tick(fps)  # Временная задержка

        # Пауза
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # пауза
                        pause = False

