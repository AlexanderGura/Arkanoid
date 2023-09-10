import pygame

class Block(pygame.sprite.Sprite):
    '''Класс, представляющий блок, который сбивает мяч.'''

    def __init__(self, color, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

class SteelBlock(Block):
    '''Класс, представляющий блок, который не может сбить мяч.'''

    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        