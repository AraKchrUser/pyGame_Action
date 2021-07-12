import pygame


class Bullet(pygame.sprite.Sprite):
    """Класс для стрелы лучника"""

    def __init__(self, ranger, *group):
        super().__init__(*group)
        self.rect = pygame.Rect(0, 0, 15, 3)
        self.rect.centerx = ranger.rect.centerx
        self.rect.center = ranger.rect.center
        self.color = (0, 0, 0)
        self.speed = 3
        self.x = float(self.rect.x)

    def update(self, origin='+'):
        if origin == '+':
            self.x += self.speed
        else:
            self.x -= self.speed
        self.rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
