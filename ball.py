import pygame
from header import *

class Ball(pygame.sprite.Sprite):
    '''Класс, представляющий мяч.'''

    def __init__(self):
        super().__init__()
        # Создание объектов Rect для представления мяча и платформы.
        # Перемещения мяча в центр экрана, а платформы в середину нижней границы.
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)
