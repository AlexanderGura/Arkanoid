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
        self.next_button = Button("Next")
        self.next_button.rect.center = self.play_button.rect.center
        self.restart_button = Button("Restart")
        self.restart_button.rect.center = self.next_button.rect.center

    def hide_main_menu(self):
        self.play_button.rect.x = -1000
        self.play_button.rect.y = -1000
        self.quit_button.rect.x = -1000
        self.quit_button.rect.y = -1000

    def hide_level_menu(self):
        self.next_button.rect.x = -1000
        self.next_button.rect.y = -1000
        self.restart_button.rect.x = -1000
        self.restart_button.rect.y = -1000

    def seek_main_menu(self):
        self.play_button.rect.center = self.screen_rect.center
        self.quit_button.rect.midtop = self.play_button.rect.midbottom

    def seek_level_menu(self):
        self.next_button.rect.center = self.screen_rect.center
        self.restart_button.rect.midtop = self.next_button.rect.midbottom

    def draw_main_menu(self):
        ''''''
        self.screen.blit(self.play_button.image, self.play_button.rect)
        self.screen.blit(self.quit_button.image, self.quit_button.rect)        

    def draw_level_menu(self):
        ''''''
        self.screen.blit(self.restart_button.image, self.restart_button.rect)
        self.screen.blit(self.next_button.image, self.next_button.rect)        