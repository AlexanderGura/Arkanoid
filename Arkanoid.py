import pygame, sys

from header import *
from block import *
from ball import *
from scoreboard import *

pygame.init()

def check_event(event):
    global platform_moving_left, platform_moving_right, game_active

    # Закрытие окна по нажатию крестика в углу окна.
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    # Обработка нажатых клавиш клавиатуры.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            platform_moving_right = True
        elif event.key == pygame.K_LEFT:
            platform_moving_left = True
        elif event.key == pygame.K_ESCAPE:
            game_active = False
        elif event.key == pygame.K_SPACE:
            ball.on_platform = False

    # Обработка поднятых(после нажатия) клавиш клавиатуры.
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            platform_moving_right = False
        elif event.key == pygame.K_LEFT:
            platform_moving_left = False

    # Обработка нажатия кнопки мыши.
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Если нажата кнопка Play, то запускается игра.
        if play_button_rect.collidepoint(pygame.mouse.get_pos()):
            game_active = True
            select_sound.play()
        # Если нажата кнопка Quit, то выходим из игры.
        if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            select_sound.play()
            pygame.quit()
            sys.exit()

def create_blocks(level_scheme):
    '''Функция отвечает за построение сетки блоков.'''
    space_block_x = BLOCK_WIDTH + BLOCK_INDENT
    space_block_y = BLOCK_HEIGHT + BLOCK_INDENT

    # Подстчёт доступного количества блоков в строке и столбце.
    available_block_x = (SCREEN_WIDTH - BALL_SIZE) // space_block_x
    available_block_y = (SCREEN_HEIGHT // 2) // space_block_y
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
                    blocks.add(block)
                elif type_block == -1:
                    steel_blocks.add(block)

def platform_movement():
    # Движения платформы (направо x увеличивается, налево - уменьшается).
    if ball.on_platform:
        if platform_moving_right and platform.x < SCREEN_WIDTH - PLATFORM_WIDTH:
            platform.x += PLATFORM_SPEED
            ball.rect.x += PLATFORM_SPEED
        if platform_moving_left and platform.x > 0:
            platform.x -= PLATFORM_SPEED
            ball.rect.x -= PLATFORM_SPEED
    else:
        if platform_moving_right and platform.x < SCREEN_WIDTH - PLATFORM_WIDTH:
            platform.x += PLATFORM_SPEED
        if platform_moving_left and platform.x > 0:
            platform.x -= PLATFORM_SPEED

def ball_bounce():
    global game_active

    # Обработка отскока от стен (столкновение == изменение направления полета).
    if ball.rect.y <= 0:
        ball.vertical = not ball.vertical
        ball_bounce_sound.play()
    elif ball.rect.x <= 0:
        ball.horizontal = not ball.horizontal
        ball_bounce_sound.play()
    elif ball.rect.right >= screen_rect.right:
        ball.horizontal = not ball.horizontal
        ball_bounce_sound.play()
    elif ball.rect.bottom >= screen_rect.bottom:
        print('yes')
        ball.float_x, ball.float_y = screen_rect.center
        ball_fall_sound.play()
        game_active = score_board.lose_heart()

def ball_movement():
    # Движения мяча - сначала изменяем дробные значения координат
    # После - координаты основного прямоугольника.
    # Движение наискос в правый нижний угол.
    if not ball.on_platform:
        if ball.vertical and ball.horizontal:
            ball.float_y += BALL_SPEED
            ball.float_x += BALL_SPEED
        # Движение наискос в правый верхний угол.
        elif not ball.vertical and ball.horizontal:
            ball.float_y -= BALL_SPEED
            ball.float_x += BALL_SPEED
        # Движение наискос в левый нижний угол.
        elif ball.vertical and not ball.horizontal:
            ball.float_y += BALL_SPEED
            ball.float_x -= BALL_SPEED
        # Движение наискос в левый верхний угол.
        else:
            ball.float_y -= BALL_SPEED
            ball.float_x -= BALL_SPEED

        ball.rect.y = ball.float_y
        ball.rect.x = ball.float_x
    else:
        ball_x, ball_y = platform.midtop
        ball.x = ball_x - BALL_SIZE // 2
        ball.y = ball_y - 60

def check_ball_platfrom_collide():

    # Если мяч столкнулся с платформой или с верхней границев, 
    # То происходит смена движения мяча.
    if not ball.on_platform and ball.rect.colliderect(platform):
        print('yes')
        ball.vertical = not ball.vertical
        ball_bounce_sound.play()

def check_ball_blocks_collide():
    # Проверка на коллизию между мячом и блоками, если они не закончились.
    # Функция возвращает список спрайтов, с которыми столкнулся мяч.
    # Флаг True означает уничтожение блока, после соприкосновения.
    if blocks:
        if pygame.sprite.spritecollide(ball, steel_blocks, False):
            ball.vertical = not ball.vertical
            hit_sound.play()

        if pygame.sprite.spritecollide(ball, blocks, True):
            ball.vertical = not ball.vertical
            hit_sound.play()
            score_board.update_score()
    else:
        score_board.update_level()
        start_new_level()

def start_new_level():
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

def update_screen():
    # Заливка экрана черным цветом, квадратов мяча и платформы белым.
    screen.fill((0, 0, 0), screen_rect)
    if game_active:
        screen.fill((255, 255, 255), ball)
        screen.fill((255, 255, 255), platform)
        blocks.draw(screen)
        steel_blocks.draw(screen)
        score_board.update(screen)
    else:
        screen.blit(play_button_image, play_button_rect)
        screen.blit(quit_button_image, quit_button_rect)        

    # Обновление экрана после каждого прохода цикла.
    pygame.display.flip()

# Создание экрана и получение поверхности и квадрата окна.
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()

# Создание кнопок Play, Quit.
font = pygame.font.SysFont(None, 72)
play_button_image = font.render("Play", True, (255, 255, 255), (0, 255, 0))
play_button_rect = play_button_image.get_rect()
play_button_rect.center = screen_rect.center

quit_button_image = font.render("Quit", True, (255, 255, 255), (255, 0, 0))
quit_button_rect = play_button_image.get_rect()
quit_button_rect.x = play_button_rect.x
quit_button_rect.y = play_button_rect.y + BUTTON_HEIGHT * 2

platform = pygame.Rect(0, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform.midbottom = screen_rect.midbottom

ball_x, ball_y = platform.midtop
ball = Ball(ball_x - BALL_SIZE // 2, ball_y - 60)

# Создание группы блоков, определение пространства для одного блока(по x, по y).
blocks = pygame.sprite.Group()
steel_blocks = pygame.sprite.Group()
create_blocks(LEVEL_1)

hit_sound = pygame.mixer.Sound('sounds/hit_block.wav')
ball_bounce_sound = pygame.mixer.Sound('sounds/ball_bounce.wav')
ball_fall_sound = pygame.mixer.Sound('sounds/ball_fall.wav')
select_sound = pygame.mixer.Sound('sounds/select.wav')

score_board = ScoreBoard()

# Основной цикл игры.
while True:
    # Цикл для проверки событий клавиатуры, мыши, окна.
    for event in pygame.event.get():
        check_event(event)

    if game_active:
        platform_movement()
        if not ball.on_platform:
            ball_movement()
            ball_bounce()
            check_ball_platfrom_collide()
            check_ball_blocks_collide()

    update_screen()