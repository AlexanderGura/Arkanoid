import pygame

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