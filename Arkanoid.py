import pygame, sys

from header import *
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

        # Создание кнопок Play, Quit.
        self.font = pygame.font.SysFont(None, 72)
        self.play_button_image = self.font.render("Play", True, (255, 255, 255), (0, 255, 0))
        self.play_button_rect = self.play_button_image.get_rect()
        self.play_button_rect.center = self.screen_rect.center

        self.quit_button_image = self.font.render("Quit", True, (255, 255, 255), (255, 0, 0))
        self.quit_button_rect = self.play_button_image.get_rect()
        self.quit_button_rect.x = self.play_button_rect.x
        self.quit_button_rect.y = self.play_button_rect.y + BUTTON_HEIGHT * 2

        self.select_sound = pygame.mixer.Sound('sounds/select.wav')
        self.score_board = ScoreBoard(self)

        self.ball = Ball(self.screen, 0, 0)
        self.platform = Platform(self)

        # Создание группы блоков, определение пространства для одного блока(по x, по y).
        self.blocks = pygame.sprite.Group()
        self.steel_blocks = pygame.sprite.Group()
        self._read_level_schemes()
        self.create_blocks()

        # Флаги состояния игры.
        self.game_active = False

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
            self.game_active = False
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
            self.game_active = True
            self.select_sound.play()

        # Если нажата кнопка Quit, то выходим из игры.
        if self.quit_button_rect.collidepoint(mouse_pos):
            self.select_sound.play()
            pygame.quit()
            sys.exit()

    def create_blocks(self):
        '''Функция отвечает за построение сетки блоков.'''
        level_scheme = self.schemes[self.score_board.level]
        space_block_x = BLOCK_WIDTH + BLOCK_INDENT
        space_block_y = BLOCK_HEIGHT + BLOCK_INDENT

        # Подстчёт доступного количества блоков в строке и столбце.
        available_block_x = (self.screen_width - BALL_SIZE) // space_block_x
        available_block_y = (self.screen_height // 2) // space_block_y
        # Заполнение строки блоками.
        for block_row in range(available_block_y):
            for block_number in range(available_block_x):
                type_block = level_scheme[block_row][block_number]
                # Если тип блока равен 0, то это пустота.
                if type_block != 0:
                    # Если тип блока равен 1, то это обычный блок.
                    if type_block == 1:
                        block = Block(BLOCK_COLOR, BLOCK_WIDTH, BLOCK_HEIGHT)
                    # Если тип блока равен 1, то это стальной блок.
                    elif type_block == -1:
                        block = SteelBlock(STEEL_BLOCK_COLOR, BLOCK_WIDTH, BLOCK_HEIGHT)

                    # Позиция блока - отступ (BALL_SIZE // 2) + 
                    # + пространство для него умноженное на номер в строке.
                    block.rect.x = 40 + BLOCK_INDENT + space_block_x * block_number
                    block.rect.y = BLOCK_INDENT * 2 + space_block_y * block_row

                    if type_block == 1:
                        self.blocks.add(block)
                    elif type_block == -1:
                        self.steel_blocks.add(block)

    def start_new_level(self):
        '''Функция используется, когда игрок перешел на новый уровень.'''
        if score_board.level == 2:
            create_blocks(LEVEL_2)
        elif score_board.level == 3:
            create_blocks(LEVEL_3)
        elif score_board.level == 4:
            create_blocks(LEVEL_4)
        elif score_board.level == 5:
            create_blocks(LEVEL_5)

        ball.center = screen_rect.center

    def update_screen(self):
        # Заливка экрана черным цветом, квадратов мяча и платформы белым.
        self.screen.fill((0, 0, 0), self.screen_rect)
        if self.game_active:
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

            if self.game_active:
                self.platform.platform_movement()
                if not self.ball.on_platform:
                    self.ball.movement()
                    self.ball.bounce()
                    self.ball.check_platfrom_collide()
                    self.ball.check_blocks_collide()

            self.update_screen()

arkanoid = Arkanoid()
arkanoid.run_game()