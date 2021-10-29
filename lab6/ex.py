import math
from random import randint as rnd
from random import choice

import pygame

pygame.init()

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
TARGET_NUMBER = 3
FONT = pygame.font.Font(None, 30)

G = 1


class Ball:
    FLOOR = 550
    WALL = 800
    bullets = []

    def __init__(self, ball_screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = ball_screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.time = -1

    def new_bullet(self, bullet_gun):
        """
        создание пули
        :param bullet_gun: выбор объекта gun
        """
        self.r += 5
        bullet_gun.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        self.vx = bullet_gun.f2_power * math.cos(bullet_gun.an)
        self.vy = - bullet_gun.f2_power * math.sin(bullet_gun.an)
        self.time = 100
        Ball.bullets.append(self)
        bullet_gun.f2_on = 0
        bullet_gun.f2_power = 10

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= G
        if (self.y >= Ball.FLOOR - self.r) and (self.vy < 0):
            if abs(self.vy) < 2:
                self.vy = 0
                self.y = Ball.FLOOR - self.r
            else:
                self.vy *= -0.5
            self.vx *= 0.5
        if self.x >= Ball.WALL - self.r:
            self.vx = -abs(self.vx)
        self.x += self.vx
        self.y -= self.vy
        self.time -= 1
        if self.time <= 0:
            self.r = 0

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 > (self.r + obj.r) ** 2:
            return False
        else:
            return True


class Gun:
    width = 10
    length_start = 10
    d_length = 1

    def __init__(self, gun_screen):
        """
        :param gun_screen: плоскость, на которой будет выведен объект
        """
        self.screen = gun_screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self):
        """
        начало заряда
        """
        self.f2_on = 1

    def fire2_end(self):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        Ball(self.screen).new_bullet(self)

    def target_getting(self, event_end):
        """Прицеливание. Зависит от положения мыши."""
        if event_end:
            self.an = math.atan((event_end.pos[1] - 450) / (event_end.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        length = Gun.length_start + self.f2_power * Gun.d_length
        gun_texture = pygame.surface.Surface((round(length) * 2, round(Gun.width)))
        gun_texture.fill(WHITE)
        pygame.draw.rect(gun_texture, self.color, (length, 0, length, Gun.width))
        rotated_gun = pygame.transform.rotate(gun_texture, -self.an * 180 / math.pi)
        self.screen.blit(rotated_gun, rotated_gun.get_rect(center=(20, 450)))

    def power_up(self):
        """
        увеличение заряда (мощности выстрела)
        """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    points = 0

    def __init__(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color = RED
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        Target.points += points
        self.live -= 1
        if self.live <= 0:
            self.r = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x >= WIDTH - self.r:
            self.vx = -abs(self.vx)
        if self.x <= self.r:
            self.vx = abs(self.vx)
        if self.y >= HEIGHT - self.r:
            self.vy = -abs(self.vy)
        if self.y <= self.r:
            self.vy = abs(self.vy)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


def text_render(text):
    return FONT.render(text, False, BLACK)


def draw_score():
    score_text = text_render(str(Target.points))
    screen.blit(score_text, (10, 10))


def draw_number_bullet():
    score_text = text_render(str(bullet) + " выстрелов вам понадобилось")
    screen.blit(score_text, (50, 270))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0

clock = pygame.time.Clock()
gun = Gun(screen)
targets = []
for i in range(TARGET_NUMBER):
    targets += [Target()]
finished = False
stop_time = 0
live_sum = True

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.draw()
    for b in Ball.bullets:
        b.draw()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end()
            bullet += 1
        elif event.type == pygame.MOUSEMOTION:
            gun.target_getting(event)

    for b in Ball.bullets:
        b.move()
        if stop_time <= 0:
            live_sum = False
            for t in range(len(targets)):
                if targets[t].live:
                    live_sum = True
                    if b.hit_test(targets[t]):
                        targets[t].hit()
                        if targets[t].live <= 0:
                            target = Target()
    for t in targets:
        t.move()
    if not live_sum:
        stop_time = 90
        live_sum = True

    if stop_time > 0:
        draw_number_bullet()
        stop_time -= 1
        if stop_time <= 0:
            targets = []
            for i in range(TARGET_NUMBER):
                targets += [Target()]
            bullet = 0

    gun.power_up()
    draw_score()
    pygame.display.update()


pygame.quit()
