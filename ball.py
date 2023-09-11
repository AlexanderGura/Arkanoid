import pygame
import random

from header import *

class Ball(pygame.sprite.Sprite):
    '''Класс, представляющий мяч.'''

    def __init__(self, screen, x, y):
        super().__init__()
        # Создание объектов Rect для представления мяча и платформы.
        # Перемещения мяча в центр экрана, а платформы в середину нижней границы.
        self.SIZE = 50
        self.SPEED = 0.1

        self.rect = pygame.Rect(x, y, self.SIZE, self.SIZE)
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.float_x = float(self.rect.x)
        self.float_y = float(self.rect.y)

        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Флаги движения мяча.
        # True - движения вниз, False - движения вверх.
        self.vertical = False
        # True - движение вправо, False - движения влево.
        self.horizontal = random.choice([True, False])
        self.on_platform = True

        self.hit_sound = pygame.mixer.Sound('sounds/hit_block.wav')
        self.bounce_sound = pygame.mixer.Sound('sounds/ball_bounce.wav')
        self.fall_sound = pygame.mixer.Sound('sounds/ball_fall.wav')


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
            print('yes')
            self.float_x, self.float_y = self.screen_rect.center
            self.fall_sound.play()
            game_active = score_board.lose_heart()

    def movement(self):
        # Движения мяча - сначала изменяем дробные значения координат
        # После - координаты основного прямоугольника.
        # Движение наискос в правый нижний угол.
        if not self.on_platform:
            if self.vertical and self.horizontal:
                self.float_y += self.SPEED
                self.float_x += self.SPEED
            # Движение наискос в правый верхний угол.
            elif not self.vertical and self.horizontal:
                self.float_y -= self.SPEED
                self.float_x += self.SPEED
            # Движение наискос в левый нижний угол.
            elif self.vertical and not self.horizontal:
                self.float_y += self.SPEED
                self.float_x -= self.SPEED
            # Движение наискос в левый верхний угол.
            else:
                self.float_y -= self.SPEED
                self.float_x -= self.SPEED

            self.rect.y = self.float_y
            self.rect.x = self.float_x
        else:
            self.x, self.y = platform.midtop
            self.x = self.x - self.SIZE // 2
            self.y = self.y - 60

    def check_platfrom_collide(self):

        # Если мяч столкнулся с платформой или с верхней границев, 
        # То происходит смена движения мяча.
        if not self.on_platform and self.rect.colliderect(platform):
            print('yes')
            self.vertical = not self.vertical
            self.bounce_sound.play()

    def check_blocks_collide(self):
        # Проверка на коллизию между мячом и блоками, если они не закончились.
        # Функция возвращает список спрайтов, с которыми столкнулся мяч.
        # Флаг True означает уничтожение блока, после соприкосновения.
        if blocks:
            if pygame.sprite.spritecollide(self, steel_blocks, False):
                self.vertical = not self.vertical
                self.hit_sound.play()

            if pygame.sprite.spritecollide(self, blocks, True):
                self.vertical = not self.vertical
                self.hit_sound.play()
                score_board.update_score()
        else:
            score_board.update_level()
            start_new_level()
