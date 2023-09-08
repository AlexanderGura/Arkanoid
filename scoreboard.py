import pygame
from header import *
from ball import *

class ScoreBoard():
    '''Класс, отвечающий за вывод и обновление счёта игры, жизней и уровня.'''

    def __init__(self):
        '''Конструктор, инициализирующий необходимые атрибуты табло.'''
        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (255, 255, 255)
        self.level = 1
        self.score = 0

        self.prep_text()
        self.prep_hearts()

    def prep_text(self):
        '''Подготовка текста к выводу на экран.'''
        self.level_image = self.font.render(str(self.level), True, 
            self.text_color, None)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.x = SCREEN_WIDTH - 50
        self.level_image_rect.y = 5

        self.score_image = self.font.render(str(self.score), True, 
            self.text_color, None)
        self.score_image_rect = self.level_image.get_rect()
        self.score_image_rect.x = SCREEN_WIDTH // 2
        self.score_image_rect.y = 5

    def prep_hearts(self):
        '''Подготавливает группу жизней к выводу на экран.'''
        self.hearts = pygame.sprite.Group()
        self.hearts_number = 3

        # Каждое сердце - шар красного цвета.
        for number in range(self.hearts_number):
            heart = Ball((BALL_SIZE + 10) * number, 0)
            heart.image.fill((255, 0, 0))
            self.hearts.add(heart)

    def update(self, surface):
        '''Обновляет информацию на экране - уровень, счёт, жизни.'''
        surface.blit(self.level_image, self.level_image_rect)
        surface.blit(self.score_image, self.score_image_rect)
        self.hearts.draw(surface)
