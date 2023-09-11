import pygame 

class Platform:

    def __init__(self, game):

        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.screen_width, self.screen_height = game.screen_rect.size
        self.ball = game.ball

        self.width = 200
        self.height = 20
        self.speed = 1

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_left = False
        self.moving_right = False


    def platform_movement(self):
        # Движения платформы (направо x увеличивается, налево - уменьшается).
        if self.ball.on_platform:
            if self.moving_right and self.rect.x < self.screen_width - self.width:
                self.rect.x += self.speed
                self.ball.rect.x += self.speed
            if self.moving_left and self.rect.x > 0:
                self.rect.x -= self.speed
                self.ball.rect.x -= self.speed
        else:
            if self.moving_right and self.rect.x < self.screen_width - self.width:
                self.rect.x += self.speed
            if self.moving_left and self.rect.x > 0:
                self.rect.x -= self.speed
