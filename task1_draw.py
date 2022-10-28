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

polygon(screen, BLACK, [(x_circle - radius / 2 + radius / 5 + 10, y_circle - radius / 3 - radius / 12),
                        (x_circle - radius / 2 + radius / 5 + 20, y_circle - radius / 3 - radius / 12 - 15),
                        (x_circle - radius + 10, y_circle - 2 * radius / 3 - 35),
                        (x_circle - radius, y_circle - 2 * radius / 3 - 20),])

polygon(screen, BLACK, [(x_circle + radius / 2 - radius / 6.5 - 20, y_circle - radius / 3 - radius / 12),
                       (x_circle + radius / 2 - radius / 6.5 - 25, y_circle - radius / 3 - radius / 12 - 15),
                       (x_circle + radius - 15, y_circle - 2 * radius / 3 - 8),
                       (x_circle + radius - 10, y_circle - 2 * radius / 3 + 7)])
finished = False
pygame.display.update()
clock = pygame.time.Clock()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()