import pygame, sys

from block import *
from ball import *
from platform import *
from scoreboard import *

class Arkanoid:
    '''Основной класс игры, отвечает за взаимодействие всех элементов игры.'''

    def __init__(self):
        '''Инициализирует атрибуты игры.'''
        pygame.init()

        # Создание экрана и получение поверхности и квадрата окна.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

        self.select_sound = pygame.mixer.Sound('sounds/select.wav')
        self.score_board = ScoreBoard(self)

        self.platform = Platform(self)
        self.ball = Ball(self)

        # Создание группы блоков, определение пространства для одного блока(по x, по y).
        self.blocks = pygame.sprite.Group()
        self.steel_blocks = pygame.sprite.Group()
        self._read_level_schemes()
        
        self.create_buttons()
        self.create_blocks()

    def _read_level_schemes(self):
        '''Функция считывает схемы уровней из файлов в словарь.'''
        # Файл - матрица: 1 - блок, 0 - пустота, -1 - стальной блок.
        self.schemes = {}
        for number in range(1, 6):
            # Открываем файл, подставляем номер уровня.
            file = open(f'level_schemes/level_{number}.txt')
            scheme = []

            # Проходимся по всем строкам файла и добавляем в список.
            for line in file:
                scheme.append(list(map(int, line.split())))
            # Ключ словаря - номер уровня, значение словаря - схема.
            self.schemes[number] = scheme

    def create_buttons(self):
        '''Функция отвечает за создание кнопок в главном меню.'''
        self.button_width = 200
        self.button_height = 50

        # Создание кнопок Play, Quit.
        self.font = pygame.font.SysFont(None, 72)
        self.play_button_image = self.font.render("Play", True, (255, 255, 255), None)
        self.play_button_rect = self.play_button_image.get_rect()
        self.play_button_rect.center = self.screen_rect.center

        self.quit_button_image = self.font.render("Quit", True, (255, 255, 255), None)
        self.quit_button_rect = self.play_button_image.get_rect()
        self.quit_button_rect.x = self.play_button_rect.x
        self.quit_button_rect.y = self.play_button_rect.y + self.button_height * 2

    def check_event(self, event):
        # Закрытие окна по нажатию крестика в углу окна.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Обработка нажатых клавиш клавиатуры.
        if event.type == pygame.KEYDOWN:
            self._check_keydown_event(event.key)

        # Обработка поднятых(после нажатия) клавиш клавиатуры.
        if event.type == pygame.KEYUP:
            self._check_keyup_event(event.key)

        # Обработка нажатия кнопки мыши.
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._check_mouse_event(pygame.mouse.get_pos())
            
    def _check_keydown_event(self, key):
        '''Функция обрабатывает нажатие клавиш.'''
        if key == pygame.K_RIGHT:
            self.platform.moving_right = True
        elif key == pygame.K_LEFT:
            self.platform.moving_left = True
        elif key == pygame.K_ESCAPE:
            self.score_board.game_active = False
        elif key == pygame.K_SPACE:
            self.ball.on_platform = False

    def _check_keyup_event(self, key):
        '''Функция обрабатывает поднятие(после нажатия) клавиш клавиатуры.'''
        if key == pygame.K_RIGHT:
            self.platform.moving_right = False
        elif key == pygame.K_LEFT:
            self.platform.moving_left = False

    def _check_mouse_event(self, mouse_pos):
        '''Функция обрабатывает нажатия кнопки мыши.'''
        # Если нажата кнопка Play, то запускается игра.
        if self.play_button_rect.collidepoint(mouse_pos):
            self.score_board.game_active = True
            self.select_sound.play()

        # Если нажата кнопка Quit, то выходим из игры.
        if self.quit_button_rect.collidepoint(mouse_pos):
            self.select_sound.play()
            pygame.quit()
            sys.exit()

    def create_blocks(self):
        '''Функция отвечает за построение сетки блоков.'''
        level_scheme = self.schemes[self.score_board.level]
        temp = Block()
        space_block_x = temp.width + self.ball.size // 2
        space_block_y = temp.height + self.ball.size // 2

        # Подстчёт доступного количества блоков в строке и столбце.
        available_block_x = (self.screen_width - self.ball.size) // space_block_x
        available_block_y = (self.screen_height // 2) // space_block_y
        # Заполнение строки блоками.
        for block_row in range(available_block_y):
            for block_number in range(available_block_x):
                type_block = level_scheme[block_row][block_number]
                # Если тип блока равен 0, то это пустота.
                if type_block != 0:
                    # Если тип блока равен 1, то это обычный блок.
                    if type_block == 1:
                        block = Block()
                    # Если тип блока равен 1, то это стальной блок.
                    elif type_block == -1:
                        block = SteelBlock()

                    # Позиция блока - отступ (self.ball.size // 2) + 
                    # + пространство для него умноженное на номер в строке.
                    block.rect.x = 40 + self.ball.size // 2 + space_block_x * block_number
                    block.rect.y = self.ball.size // 2 * 2 + space_block_y * block_row

                    if type_block == 1:
                        self.blocks.add(block)
                    elif type_block == -1:
                        self.steel_blocks.add(block)

    def check_platfrom_collide(self):
        # Если мяч столкнулся с платформой или с верхней границев, 
        # То происходит смена движения мяча.
        if not self.ball.on_platform and self.ball.rect.colliderect(self.platform):
            self.ball.vertical = not self.ball.vertical
            self.ball.bounce_sound.play()

    def check_blocks_collide(self):
        # Проверка на коллизию между мячом и блоками, если они не закончились.
        # Функция возвращает список спрайтов, с которыми столкнулся мяч.
        # Флаг True означает уничтожение блока, после соприкосновения.
        if self.blocks:
            if pygame.sprite.spritecollide(self.ball, self.steel_blocks, False):
                self.ball.vertical = not self.ball.vertical
                self.ball.hit_sound.play()

            if pygame.sprite.spritecollide(self.ball, self.blocks, True):
                self.ball.vertical = not self.ball.vertical
                self.ball.hit_sound.play()
                self.score_board.update_score()
        else:
            self.score_board.update_level()
            self.start_new_level()

    def start_new_level(self):
        '''Функция используется, когда игрок перешел на новый уровень.'''
        self.create_blocks()
        self.ball.on_platform = True

    def update_screen(self):
        # Заливка экрана черным цветом, квадратов мяча и платформы белым.
        self.screen.fill((0, 0, 0), self.screen_rect)
        if self.score_board.game_active:
            self.screen.fill((255, 255, 255), self.ball)
            self.screen.fill((255, 255, 255), self.platform)
            self.blocks.draw(self.screen)
            self.steel_blocks.draw(self.screen)
            self.score_board.update(self.screen)
        else:
            self.screen.blit(self.play_button_image, self.play_button_rect)
            self.screen.blit(self.quit_button_image, self.quit_button_rect)        

        # Обновление экрана после каждого прохода цикла.
        pygame.display.flip()

    def run_game(self):
        # Основной цикл игры.
        while True:
            # Цикл для проверки событий клавиатуры, мыши, окна.
            for event in pygame.event.get():
                self.check_event(event)

            if self.score_board.game_active:
                self.platform.platform_movement()
                self.ball.movement()
                self.ball.bounce()
                self.check_platfrom_collide()
                self.check_blocks_collide()

            self.update_screen()

arkanoid = Arkanoid()
arkanoid.run_game()