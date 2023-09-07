import pygame, sys

pygame.init()

# Константы.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOLL_SIZE = 40
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 20

# Создание экрана и получение поверхности и квадрата окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

# Создание объектов Rect для представления мяча и платформы.
boll = pygame.Rect(0, 0, BOLL_SIZE, BOLL_SIZE)
platform = pygame.Rect(0, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform.midbottom = screen_rect.midbottom

# Основной цикл игры.
while True:
    # Цикл для проверки событий клавиатуры, мыши, окна.ы
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Заливка квадратов мяча и платформы белым цветом.
    screen.fill((255, 255, 255), boll)
    screen.fill((255, 255, 255), platform)

    # Обновление экрана после каждого прохода цикла.
    pygame.display.update()
