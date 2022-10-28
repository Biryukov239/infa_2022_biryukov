import pygame
from pygame.draw import *

pygame.init()
screen = pygame.display.set_mode((500, 400))



pygame.display.update()

clock = pygame.time.Clock()
clock.tick(40)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()