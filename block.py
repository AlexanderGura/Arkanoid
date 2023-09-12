import pygame

class Block(pygame.sprite.Sprite):
    '''Класс, представляющий блок, который сбивает мяч.'''

    def __init__(self):
        super().__init__()

        self.width = 80
        self.height = 20
        self.color = (0, 0, 255)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

class SteelBlock(Block):
    '''Класс, представляющий блок, который не может сбить мяч.'''

    def __init__(self):
        super().__init__()
        self.color = (180, 180, 180)
        