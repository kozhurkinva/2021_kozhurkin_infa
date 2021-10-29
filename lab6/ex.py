import math
from random import randint as rnd
from random import choice

import pygame

pygame.init()

fps = 30

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
screen = pygame.display.set_mode((WIDTH, HEIGHT))

g = 1


class Ball:
    floor = HEIGHT
    walls = (0, WIDTH)

    def __init__(self, ball_screen=screen, x=40, y=450):
        """ конструктор класса ball

        args:
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

    def move(self):
        """переместить мяч по прошествии единицы времени.

        метод описывает перемещение мяча за один кадр перерисовки. то есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям экрана.
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x <= Ball.walls[0] + self.r:
            self.vx = abs(self.vx)
        if self.x >= Ball.walls[1] - self.r:
            self.vx = -abs(self.vx)
        if self.y >= Ball.floor - self.r:
            self.vy = abs(self.vx)
        if self.death_check():
            self.r = 0

    def draw(self):
        """чертит объект"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def death_check(self):
        if self.live <= 0:
            return True
        else:
            return False


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
        """начало заряда"""
        self.f2_on = 1

    def fire2_end(self):
        """выстрел мячом.

        происходит при отпускании кнопки мыши.
        начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        Bullet(self)

    def target_getting(self, event_end):
        """прицеливание. зависит от положения мыши."""
        if event_end:
            self.an = math.atan((event_end.pos[1] - 450) / (event_end.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """чертит объект"""
        length = gun.length_start + self.f2_power * gun.d_length
        gun_texture = pygame.surface.Surface((round(length) * 2, round(gun.width)))
        gun_texture.fill(WHITE)
        pygame.draw.rect(gun_texture, self.color, (length, 0, length, gun.width))
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


class Bullet(Ball):
    """
    создание пули
    :param bullet_gun: выбор объекта gun
    """
    bullets = []

    def __init__(self, bullet_gun, surface=screen):
        super().__init__(surface)
        self.r += 5
        bullet_gun.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        self.vx = bullet_gun.f2_power * math.cos(bullet_gun.an)
        self.vy = - bullet_gun.f2_power * math.sin(bullet_gun.an)
        self.live = 100
        Bullet.bullets.append(self)
        bullet_gun.f2_on = 0
        bullet_gun.f2_power = 10

    def hit_test(self, obj):
        """функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        args:
            obj: обьект, с которым проверяется столкновение.
        returns:
            возвращает true в случае столкновения мяча и цели. в противном случае возвращает false.
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 > (self.r + obj.r) ** 2) or self.death_check():
            return False
        else:
            return True

    def move(self):
        if self.y >= Ball.floor - self.r:
            self.vy *= 0.5
            self.vx *= 0.5
            if abs(self.vy < 2):
                self.vy = 0
                self.y = self.floor - self.r
        super().move()
        self.vy -= g
        self.live -= 1


class Target(Ball):
    points = 0

    def __init__(self, surface=screen):
        super().__init__(surface)
        self.live = 1
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color = RED
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)

    def hit(self, points=1):
        """попадание шарика в цель."""
        Target.points += points
        self.live -= 1

    def move(self):
        """перемещение целей"""
        super().move()
        if self.y <= self.r:
            self.vy = -abs(self.vy)


def text_render(text):
    """рендерит текст"""
    return FONT.render(text, False, BLACK)


def draw_score():
    """ресует счёт"""
    score_text = text_render(str(Target.points))
    screen.blit(score_text, (10, 10))


def draw_number_bullet():
    """рисует текст в конце каждого сеанса"""
    score_text = text_render(str(bullet) + " выстрелов вам понадобилось")
    screen.blit(score_text, (50, 270))


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

    # прорисовка основных объектов
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.draw()
    for b in Bullet.bullets:
        b.draw()

    clock.tick(fps)

    # обработка событий
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

    # обработка взаимодействия мячей и мишеней
    for b in Bullet.bullets:
        b.move()
        if stop_time <= 0:
            live_sum = False
            for t in targets:
                if t.live:
                    live_sum = True
                    if b.hit_test(t):
                        t.hit()
    for t in targets:
        t.move()

    # когда кончились мишени, нужно обработать конец игрового сеанса
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
