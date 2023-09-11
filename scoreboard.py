import pygame
from header import *
from ball import *

class ScoreBoard():
    '''Класс, отвечающий за вывод и обновление счёта игры, жизней и уровня.'''

    def __init__(self, game):
        '''Конструктор, инициализирующий необходимые атрибуты табло.'''
        self.screen = game.screen
        self.screen_rect = game.screen
        self.screen_width, self.screen_height = game.screen_rect.size

        self.font = pygame.font.SysFont(None, 48)
        self.text_color = (255, 255, 255)
        self.level = 1
        self.score = 0

        self.prep_text()
        # self.prep_hearts()

    def prep_text(self):
        '''Подготовка текста к выводу на экран.'''
        self.level_image = self.font.render(str(self.level), True, 
            self.text_color, None)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.x = self.screen_width - 50
        self.level_image_rect.y = 5

        self.score_image = self.font.render(str(self.score), True, 
            self.text_color, None)
        self.score_image_rect = self.level_image.get_rect()
        self.score_image_rect.x = self.screen_width // 2
        self.score_image_rect.y = 5

    # def prep_hearts(self):
    #     '''Подготавливает группу жизней к выводу на экран.'''
    #     self.hearts = pygame.sprite.Group()
    #     self.hearts_number = 3

    #     # Каждое сердце - шар красного цвета.
    #     for number in range(self.hearts_number):
    #         heart = Ball((BALL_SIZE + 10) * number, 0)
    #         heart.image.fill((255, 0, 0))
    #         self.hearts.add(heart)

    # def lose_heart(self):
    #     '''Функция вызывается, когда проиходит потеря жизни.'''
    #     # Получаем последнее сердце с помощью метода .sprites()
    #     # И удаляем его.
    #     if self.hearts:
    #         last_heart = self.hearts.sprites()[-1]
    #         self.hearts.remove(last_heart)
    #         return True
    #     else:
    #         return False

    def update_score(self):
        '''Функция вызывается, когда игрок получил очки.'''
        self.score += BLOCK_POINTS
        self.update_text()

    def update_level(self):
        '''Функция вызывается, когда игрок вышел на новый уровень.'''
        self.level += 1
        self.update_text()

    def update_text(self):
        '''Функция вызывается, когда происхоит изменение табло.'''
        self.level_image = self.font.render(str(self.level), True, 
            self.text_color, None)
        self.score_image = self.font.render(str(self.score), True, 
            self.text_color, None)

    def update(self, surface):
        '''Обновляет информацию на экране - уровень, счёт, жизни.'''
        surface.blit(self.level_image, self.level_image_rect)
        surface.blit(self.score_image, self.score_image_rect)
        # self.hearts.draw(surface)

