# Константы.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

BALL_SIZE = 100
BALL_SPEED = 3.3

PLATFORM_WIDTH = SCREEN_WIDTH
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 1

BLOCK_WIDTH = 100
BLOCK_HEIGHT = 20
BLOCK_INDENT = BALL_SIZE // 2
BLOCK_COLOR = (0, 0, 255)
BLOCK_POINTS = 20

# Флаги состояния игры.
ball_vertical = True      # True - движения вниз, False - движения вверх.
ball_horizontal = True    # True - движение вправо, False - движения влево.
platform_moving_left = False
platform_moving_right = False
game_active = False