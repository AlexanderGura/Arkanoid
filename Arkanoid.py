import pygame, sys

pygame.init()
screen = pygame.display.set_mode((600, 600))
screen_rect = screen.get_rect()

boll = pygame.Rect(0, 0, 40, 40)
platform = pygame.Rect(0, 0, 150, 20)
platform.midbottom = screen_rect.midbottom

while True:
    screen.fill((255, 255, 255), boll)
    screen.fill((255, 255, 255), platform)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
