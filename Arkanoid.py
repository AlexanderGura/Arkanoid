import pygame, sys

pygame.init()

# Константы.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BALL_SIZE = 40
BALL_SPEED = 0.3
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 1

# Флаги состояния игры.
ball_vertical = True      # True - движения вниз, False - движения вверх.
ball_horizontal = True    # True - движение вправо, False - движения влево.
platform_moving_left = False
platform_moving_right = False
game_active = False

# Создание экрана и получение поверхности и квадрата окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

# Создание объектов Rect для представления мяча и платформы.
# Перемещения мяча в центр экрана, а платформы в середину нижней границы.
ball = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
ball.midtop = screen_rect.midtop
ball.y += BALL_SIZE
ball_float_x = float(ball.x)
ball_float_y = float(ball.y)

platform = pygame.Rect(0, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform.midbottom = screen_rect.midbottom

# Основной цикл игры.
while True:
    # Цикл для проверки событий клавиатуры, мыши, окна.
    for event in pygame.event.get():
        # Закрытие окна по нажатию крестика в углу окна.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Обработка нажатых клавиш клавиатуры.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                platform_moving_right = True
            elif event.key == pygame.K_LEFT:
                platform_moving_left = True
            elif event.key == pygame.K_ESCAPE:
                game_active = False

        # Обработка поднятых(после нажатия) клавиш клавиатуры.
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                platform_moving_right = False
            elif event.key == pygame.K_LEFT:
                platform_moving_left = False

        # Обработка нажатия кнопки мыши.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Если нажата кнопка Play, то запускается игра.
            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                game_active = True
            # Если нажата кнопка Quit, то выходим из игры.
            if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()

    if game_active:
        # Движения платформы (направо x увеличивается, налево - уменьшается).
        if platform_moving_right and platform.x < SCREEN_WIDTH - PLATFORM_WIDTH:
            platform.x += PLATFORM_SPEED
        if platform_moving_left and platform.x > 0:
            platform.x -= PLATFORM_SPEED

        # Обработка отскока от стен (столкновение == изменение направления полета).
        if ball.y <= 0:
            ball_vertical = not ball_vertical
        if ball.x <= 0:
            ball_horizontal = not ball_horizontal
        if ball.right >= screen_rect.right:
            ball_horizontal = not ball_horizontal
        if ball.bottom >= screen_rect.bottom:
            ball_float_x, ball_float_y = screen_rect.center

        # Движения мяча - сначала изменяем дробные значения координат
        # После - координаты основного прямоугольника.
        # Движение наискос в правый нижний угол.
        if ball_vertical and ball_horizontal:
            ball_float_y += BALL_SPEED
            ball_float_x += BALL_SPEED
        # Движение наискос в правый верхний угол.
        elif not ball_vertical and ball_horizontal:
            ball_float_y -= BALL_SPEED
            ball_float_x += BALL_SPEED
        # Движение наискос в левый нижний угол.
        elif ball_vertical and not ball_horizontal:
            ball_float_y += BALL_SPEED
            ball_float_x -= BALL_SPEED
        # Движение наискос в левый верхний угол.
        else:
            ball_float_y -= BALL_SPEED
            ball_float_x -= BALL_SPEED

        ball.y = ball_float_y
        ball.x = ball_float_x

        # Если мяч столкнулся с платформой или с верхней границев, 
        # То происходит смена движения мяча.
        if ball.colliderect(platform):
            ball_vertical = not ball_vertical

    # Заливка экрана черным цветом, квадратов мяча и платформы белым.
    screen.fill((0, 0, 0), screen_rect)
    if game_active:
        screen.fill((255, 255, 255), ball)
        screen.fill((255, 255, 255), platform)
    else:
        screen.blit(play_button_image, play_button_rect)
        screen.blit(quit_button_image, quit_button_rect)        

    # Обновление экрана после каждого прохода цикла.
    pygame.display.flip()