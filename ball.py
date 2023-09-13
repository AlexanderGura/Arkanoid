import pygame
import random

class Ball(pygame.sprite.Sprite):
    '''Класс, представляющий мяч.'''

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.screen_width, self.screen_height = game.screen_rect.size
        self.score_board = game.score_board
        self.platform = game.platform

        # Создание объектов Rect для представления мяча и платформы.
        # Перемещения мяча в центр экрана, а платформы в середину нижней границы.
        self.size = 50
        self.speed = 0.5

        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.ball_to_platform()
        self.image = pygame.Surface((self.size, self.size))
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)

        # Флаги движения мяча.
        # True - движения вниз, False - движения вверх.
        self.vertical = False
        # True - движение вправо, False - движения влево.
        self.horizontal = random.choice([True, False])
        self.on_platform = True

        self.hit_sound = pygame.mixer.Sound('sounds/hit_block.wav')
        self.bounce_sound = pygame.mixer.Sound('sounds/ball_bounce.wav')
        self.fall_sound = pygame.mixer.Sound('sounds/ball_fall.wav')

    def ball_to_platform(self):
        '''Возвращает мяч к платформе.'''
        self.on_platform = True
        self.vertical = False
        self.rect.midbottom = self.platform.rect.midtop
        self.rect.y -= 50
        self.float_x, self.float_y = self.rect.x, self.rect.y

    def bounce(self):
        # Обработка отскока от стен (столкновение == изменение направления полета).
        if self.rect.y <= 0:
            self.vertical = not self.vertical
            self.bounce_sound.play()
        elif self.rect.x <= 0:
            self.horizontal = not self.horizontal
            self.bounce_sound.play()
        elif self.rect.right >= self.screen_rect.right:
            self.horizontal = not self.horizontal
            self.bounce_sound.play()
        elif self.rect.bottom >= self.screen_rect.bottom:
            self.float_x, self.float_y = self.screen_rect.center
            self.fall_sound.play()
            self.score_board.lose_heart()
            self.ball_to_platform()

    def movement(self):
        # Движения мяча - сначала изменяем дробные значения координат
        # После - координаты основного прямоугольника.
        # Движение наискос в правый нижний угол.
        if not self.on_platform:
            if self.vertical and self.horizontal:
                self.float_y += self.speed
                self.float_x += self.speed
            # Движение наискос в правый верхний угол.
            elif not self.vertical and self.horizontal:
                self.float_y -= self.speed
                self.float_x += self.speed
            # Движение наискос в левый нижний угол.
            elif self.vertical and not self.horizontal:
                self.float_y += self.speed
                self.float_x -= self.speed
            # Движение наискос в левый верхний угол.
            else:
                self.float_y -= self.speed
                self.float_x -= self.speed

            self.rect.y = self.float_y
            self.rect.x = self.float_x
        else:
            self.ball_to_platform()