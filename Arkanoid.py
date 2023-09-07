import pygame, sys

pygame.init()

# Константы.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOLL_SIZE = 40
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 1

# Флаги состояния игры.
platform_moving_left = False
platform_moving_right = False

# Создание экрана и получение поверхности и квадрата окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

# Создание объектов Rect для представления мяча и платформы.
boll = pygame.Rect(0, 0, BOLL_SIZE, BOLL_SIZE)
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                platform_moving_right = True
            elif event.key == pygame.K_LEFT:
                platform_moving_left = True

        # Обработка поднятых(после нажатия) клавиш клавиатуры.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                platform_moving_right = False
            elif event.key == pygame.K_LEFT:
                platform_moving_left = False

    # Движения платформы (направо x увеличивается, налево - уменьшается).
    if platform_moving_right:
        platform.x += PLATFORM_SPEED
    if platform_moving_left:
        platform.x -= PLATFORM_SPEED

    # Заливка экрана черным цветом, квадратов мяча и платформы белым.
    screen.fill((0, 0, 0), screen_rect)
    screen.fill((255, 255, 255), boll)
    screen.fill((255, 255, 255), platform)

    # Обновление экрана после каждого прохода цикла.
    pygame.display.flip()