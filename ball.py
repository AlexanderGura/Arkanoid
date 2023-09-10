import pygame
import random

from header import *

class Ball(pygame.sprite.Sprite):
    '''Класс, представляющий мяч.'''

    def __init__(self, x, y):
        super().__init__()
        # Создание объектов Rect для представления мяча и платформы.
        # Перемещения мяча в центр экрана, а платформы в середину нижней границы.
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.rect.x = x
        self.rect.y = y
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)

        # Флаги движения мяча.
        # True - движения вниз, False - движения вверх.
        self.vertical = False
        # True - движение вправо, False - движения влево.
        self.horizontal = random.choice([True, False])
        self.on_platform = True