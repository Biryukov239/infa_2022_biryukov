import pygame
from pygame.draw import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
x_circle = 200
y_circle = 175
radius = 150
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill(WHITE)
pygame.display.flip()
circle(screen, (255, 255, 0), (x_circle, y_circle), radius)
circle(screen, (255, 0, 0), (x_circle - radius / 2, y_circle - radius / 3), radius / 5)
circle(screen, BLACK, (x_circle - radius / 2, y_circle - radius / 3), radius / 12)

circle(screen, (255, 0, 0), (x_circle + radius / 2, y_circle - radius / 3), radius / 6.5)
circle(screen, BLACK, (x_circle + radius / 2, y_circle - radius / 3), radius / 12)

rect(screen, BLACK, (x_circle - radius / 2, y_circle + radius * 1 / 2, 150, 30))

polygon(screen, BLACK, [(x_circle - radius, y_circle - 0.8 * radius), (x_circle - radius - 5, y_circle - 0.8 * radius + 5),
                               (x_circle - 20, y_circle - 50), (x_circle - 15, y_circle - 55)])

finished = False
pygame.display.update()
clock = pygame.time.Clock()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()