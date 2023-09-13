import pygame
from ball import *

class Heart(pygame.sprite.Sprite):
    '''Класс, представляющий жизнь игрока.'''
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()


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
        self.block_points = 50

        # Флаги состояния игры.
        self.game_active = False
        self.free_throw = True

        self.prep_text()

        self.hearts = pygame.sprite.Group()
        self.hearts_number = 3
        self.prep_hearts()

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

    def prep_hearts(self):
        '''Подготавливает группу жизней к выводу на экран.'''
        # Каждое сердце - шар красного цвета.
        for number in range(self.hearts_number):
            heart = Heart()
            heart.rect.x = 50 + (heart.rect.width * 2) * number
            self.hearts.add(heart)

    def lose_heart(self):
        '''Функция вызывается, когда проиходит потеря жизни.'''
        # Получаем последнее сердце с помощью метода .sprites()
        # И удаляем его.
        if self.hearts:
            self.hearts.remove(self.hearts.sprites()[-1])
            self.game_active = True
        else:
            self.game_active = False

    def update(self):
        '''Функция вызывается, когда происхоит изменение табло.'''
        self.level_image = self.font.render(str(self.level), True, 
            self.text_color, None)
        self.score_image = self.font.render(str(self.score), True, 
            self.text_color, None)

    def draw(self):
        '''Обновляет информацию на экране - уровень, счёт, жизни.'''
        self.screen.blit(self.level_image, self.level_image_rect)
        self.screen.blit(self.score_image, self.score_image_rect)
        self.hearts.draw(self.screen)