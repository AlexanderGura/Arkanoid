import pygame

class Button():
    ''''''
    def __init__(self, text):
        self.font = pygame.font.SysFont(None, 72)
        self.image = self.font.render(text, True, (255, 255, 255), None)
        self.rect = self.image.get_rect()

class Menu():
    '''Определение класса, отвечающего за меню.'''
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen_rect
        self.screen_width, self.screen_height = game.screen_rect.size

        self.button_width = 200
        self.button_height = 50

        # Создание кнопок Play, Quit.
        self.play_button = Button("Play")
        self.play_button.rect.center = self.screen_rect.center
        self.quit_button = Button("Quit")
        self.quit_button.rect.midtop = self.play_button.rect.midbottom

        # Создание кнопок Restart, Next.
        self.restart_button = Button("Play")
        self.next_button = Button("Quit")

    def draw(self):
        ''''''
        self.screen.blit(self.play_button.image, self.play_button.rect)
        self.screen.blit(self.quit_button.image, self.quit_button.rect)        