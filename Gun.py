import math
import numpy as np
from random import choice, randint
import pygame
import time

pygame.init()
FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

my_font = pygame.font.SysFont('Comic Sans MS', 30)
trace = ([])
fl = 1
def draw_point(m, col, screen):
    for [i, j] in m:
        pygame.draw.circle(
            screen,
            col,
            (i, j),
            1
        )

def dist(x1, y1, x2, y2):
   return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 9
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.trace = trace

    def change_v(self):
        '''
        Функция меняет скорость у шарика
        в зависимости от его положения(с какой именно стеной он столкнулся)
        '''
        k = 0.7
        if (self.x < self.radius + 10) and (self.y < self.radius + 10):
            self.vx = math.sqrt((self.vx ** 2 + self.vy ** 2) / 2)
            self.vy = math.sqrt((self.vx ** 2 + self.vy ** 2) / 2)
        elif (self.x > WIDTH - self.radius - 10) and (self.y > HEIGHT - self.radius - 10):
            self.vx = -math.sqrt((self.vx ** 2 + self.vy ** 2) / 2)
            self.vy = -math.sqrt((self.vx ** 2 + self.vy ** 2) / 2)
        elif (self.x < self.radius + 10) and (self.y > HEIGHT - self.radius - 10):
            self.vx = math.sqrt((self.vx ** 2 + self.vy ** 2) / 2)
            self.vy = -math.sqrt((self.vx ** 2 + self.vy ** 2) / 2)
        elif (self.x > WIDTH - self.radius - 10) and (self.y < self.radius + 10):
            self.vx = -math.sqrt((self.vx ** 2 + self.vy ** 2) / 2)
            self.vy = math.sqrt((self.vx ** 2 + self.vy ** 2) / 2)
        elif (self.x < self.radius + 10) or (self.x > WIDTH - self.radius - 10):
            self.vx = -k * self.vx
            self.vy *= k
        elif (self.y < self.radius + 10) or (self.y > HEIGHT - self.radius - 10):
            self.vy = -k * self.vy
            self.vx *= k

    def is_stop(self):
        """Проверяет не остановился лт шарик"""
        return self.vx ** 2 + self.vy ** 2 < 1


    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        g = 1

        self.trace.append([self.x, self.y])
        draw_point(trace, self.color, self.screen)
        if not self.is_stop():
            self.x += self.vx
            self.vy += g
            self.y += self.vy
            if self.isCol():
                self.fix_position()
                self.change_v()
        else:
            self.fix_position()

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.radius
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        d = dist(self.x, self.y, obj.x, obj.y)
        if d <= 1.2*(self.radius + obj.radius):
            return True
        else:
            return False

    def isCol(self):
        """Функция проверяет, сталкивалкивается ли шарик со стеной.
        Returns:
            Возвращает True в случае столкновения мяча и стены. В противном случае возвращает False.
        """
        delta = 1
        if (self.y > self.radius + delta) and (self.y < HEIGHT - self.radius - delta) and (self.x > self.radius + delta) and (
                self.x < WIDTH - self.radius - delta):
            return False
        else:
            return True

    def fix_position(self):
        '''
        Исправляет позицию шарика при коллизии,
        чтобы избежать проблем, связанных в краевыми эффектами
        '''
        delta1 = 5
        if self.x < delta1 + self.radius:
            self.x = delta1 + self.radius
        if self.x > WIDTH - self.radius - delta1:
            self.x = WIDTH - self.radius - delta1
        if self.y < delta1 + self.radius:
            self.y = delta1 + self.radius
        if self.y > HEIGHT - self.radius - delta1:
            self.y = HEIGHT - self.radius - delta1


def rot(an, p0, p1):
    x1_rot = p0[0] + (p1[0] - p0[0]) * math.cos(an) - (p1[1] - p0[1]) * math.sin(an)
    y1_rot = p0[1] + (p1[0] - p0[0]) * math.sin(an) + (p1[1] - p0[1]) * math.cos(an)
    return np.array([x1_rot, y1_rot])


class Gun:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450
        self.length = 30

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball(self.screen)
        new_ball.radius += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] - 20 != 0:
                self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
            elif event.pos[1] < 450:
                self.an = math.pi / 2
            elif event.pos[1] >= 450:
                self.an = -math.pi / 2
        limit_len = 100
        if self.f2_on:
            self.color = RED
            if self.length < limit_len:
                self.length += 1
        else:
            self.length = 30
            self.color = GREY

    def draw(self):
        width = 10
        p0 = np.array([20, 450])
        p1 = p0 + np.array([self.length, 0])
        p2 = p0 + np.array([0, width])

        p1_rot = rot(self.an, p0, p1)
        p2_rot = rot(self.an, p0, p2)
        p3_rot = p1_rot + p2_rot - p0
        pygame.draw.polygon(self.screen, self.color, [p2_rot, p0, p1_rot, p3_rot])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 59:
                self.f2_power += 0.7
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.radius = randint(8, 20)
        self.color = GAME_COLORS[randint(0, len(GAME_COLORS)) - 1]

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.radius = randint(5, 20)
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.radius
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
list_of_motions = []

clock = pygame.time.Clock()
t11 = 0
t2 = 0
flag1 = 0
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()


    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and fl != 0:
            gun.fire2_start(event)
            trace = ([])
            Ball.trace = ([])

        elif event.type == pygame.MOUSEBUTTONUP and fl != 0:
            gun.fire2_end(event)
            bullet += 1
        elif event.type == pygame.MOUSEMOTION and fl != 0:
            gun.targetting(event)
            list_of_motions.append(event)

    if len(list_of_motions) != 0:
        gun.targetting(list_of_motions[-1])
    text_surface1 = my_font.render(f'Вы уничтожили цель за {bullet} выстрелов', False, (0, 0, 0))

    text_surface2 = my_font.render(f'{target.points}', False, (0, 0, 0))

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            t11 = time.time()
            target.hit()
            target.new_target()
            flag1 = 0

    t2 = time.time()

    if t2 - t11 <= 2:
        screen.blit(text_surface1, (100, HEIGHT // 3))
        fl = 0
    elif flag1 == 0:
        bullet = 0
        balls = []
        flag1 = 1
        fl = 1
    screen.blit(text_surface2, (50, 50))
    pygame.display.update()
    gun.power_up()

pygame.quit()