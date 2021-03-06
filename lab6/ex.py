import math
from random import randint as rnd
from random import choice

import pygame

pygame.init()

fps = 30

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 201, 31)
GREEN = (0, 255, 0)
MAGENTA = (255, 3, 184)
CYAN = (0, 255, 204)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
target_number = 3
FONT = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

G = 1


class Circle:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r


class Ball(Circle):
    FLOOR = HEIGHT
    WALLS = (0, WIDTH)

    def __init__(self, ball_screen=screen, x=40, y=450, r=10):
        """ конструктор класса ball

        args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = ball_screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.circles = [Circle(x, y, r)]

    def move(self):
        """переместить мяч по прошествии единицы времени.

        метод описывает перемещение мяча за один кадр перерисовки. то есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy и стен по краям экрана.
        """
        self.x += self.vx
        self.y -= self.vy
        if self.x <= self.WALLS[0] + self.r:
            self.vx = abs(self.vx)
            self.x = self.WALLS[0] + self.r
        if self.x >= self.WALLS[1] - self.r:
            self.vx = -abs(self.vx)
            self.x = self.WALLS[1] - self.r
        if self.y >= self.FLOOR - self.r:
            self.vy = abs(self.vy)
            self.y = self.FLOOR - self.r
        self.circles = [Circle(self.x, self.y, self.r)]

    def draw(self):
        """чертит объект"""
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 1)

    def death_check(self):
        if self.live <= 0:
            self.r = 0
            return True
        else:
            return False


class Gun:
    width = 10
    length_start = 10
    d_length = 1

    def __init__(self, gun_screen, x=40, y=450):
        """
        :param gun_screen: плоскость, на которой будет выведен объект
        """
        self.screen = gun_screen
        self.f2_power = 10
        self.f2_on = 0
        self.move_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.y = y

    def fire2_start(self):
        """начало заряда"""
        self.f2_on = 1

    def fire2_end(self):
        """выстрел мячом.

        происходит при отпускании кнопки мыши.
        начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        Cannonball(self)

    def target_getting(self, event_end):
        """прицеливание. зависит от положения мыши."""
        if event_end:
            if event_end.pos[0] != self.x:
                self.an = math.atan((event_end.pos[1] - self.y) / (event_end.pos[0] - self.x))
                self.an += int(event_end.pos[0] < self.x) * math.pi
            else:
                self.an = math.pi / 2 * - (int(event_end.pos[1] < self.y) * 2 - 1)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def move_start(self):
        """начало движения"""
        self.move_on = 1

    def move_end(self):
        """остановка"""
        self.move_on = 0

    def move(self):
        """перемещение. зависит от положения мыши."""
        if self.move_on:
            self.x += math.cos(self.an) * 3
            self.y += math.sin(self.an) * 3

    def draw_gun(self):
        length = gun.length_start + self.f2_power * gun.d_length
        gun_texture = pygame.Surface((round(length) * 2, round(gun.width)), pygame.SRCALPHA)
        pygame.draw.rect(gun_texture, self.color, (length, 0, length, gun.width))
        rotated_gun = pygame.transform.rotate(gun_texture, -self.an * 180 / math.pi)
        self.screen.blit(rotated_gun, rotated_gun.get_rect(center=(self.x, self.y)))

    def draw(self):
        """чертит объект"""
        pygame.draw.circle(screen, YELLOW, (self.x, self.y - 80), 50)
        pygame.draw.circle(screen, BLACK, (self.x, self.y - 80), 50, 1)
        shar_texture(self.x, self.y - 80, 50, RED)
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)
        self.draw_gun()

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

    def possibility_check(self):
        """проверяет возможность стрельбы"""
        return True


class Bomber(Gun):

    def fire2_end(self):
        Bomb(self)

    def draw(self):
        airship_texture(self.x, self.y, 30, math.cos(self.an), YELLOW, RED)


class LaserGun(Gun):

    def possibility_check(self):
        if self.y < HEIGHT - 22:
            return False
        else:
            return True

    def draw(self):
        if not self.possibility_check():
            parachute_texture(self.x, self.y, 30)
        else:
            pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x - 11, self.y + 22))
            pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x, self.y + 22))
            pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x + 11, self.y + 22))
            self.draw_gun()

    def move(self):
        if not self.possibility_check():
            self.move_on = 1
            super().move()
            self.y += 3

    def move_start(self):
        pass

    def move_end(self):
        pass

    def target_getting(self, event_end):
        if not self.f2_on:
            super().target_getting(event_end)

    def fire2_end(self):
        if self.f2_power >= 90:
            Laser(self)
            self.f2_power = 10
            self.f2_on = 0

    def power_up(self):
        super(LaserGun, self).power_up()
        if self.f2_power >= 90:
            self.fire2_end()


class Bullet(Ball):
    """
    создание пули
    :param bullet_gun: выбор объекта gun
    """
    bullets = []
    JUMP = 0.6

    def __init__(self, bullet_gun, surface=screen):
        super().__init__(surface, bullet_gun.x, bullet_gun.y)
        self.r += 5
        bullet_gun.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        self.vx = bullet_gun.f2_power * math.cos(bullet_gun.an)
        self.vy = - bullet_gun.f2_power * math.sin(bullet_gun.an)
        self.live = 200
        Bullet.bullets.append(self)
        bullet_gun.f2_on = 0
        bullet_gun.f2_power = 10

    def hit_test(self, circle):
        """функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        args:
            obj: обьект, с которым проверяется столкновение.
        returns:
            возвращает true в случае столкновения мяча и цели. в противном случае возвращает false.
        """
        test = False
        number = 0
        dx, dy = self.x - circle.x, self.y - circle.y
        if self.r != 0:
            while ((number * self.r <= (self.vx ** 2 + self.vy ** 2) ** 0.5) and
                   (self.vx ** 2 + self.vy ** 2 != 0) and
                   (self.r != 0)):
                k = self.r / (self.vx ** 2 + self.vy ** 2) ** 0.5
                dx, dy = self.x - k * self.vx - circle.x, self.y + k * self.vy - circle.y
                if (dx ** 2 + dy ** 2 <= (self.r + circle.r) ** 2) and not self.death_check():
                    test = True
                number += 0.5
            if (dx ** 2 + dy ** 2 <= (self.r + circle.r) ** 2) and not self.death_check():
                test = True
        return test

    def hit_reaction(self):
        """реакция пули на попадание в цель"""
        pass

    def move(self):
        if self.y >= self.FLOOR - self.r:
            if self.vy >= 0:
                self.vy *= self.JUMP
                self.vx *= self.JUMP
                if abs(self.vy < 2):
                    self.vy = 0
                    self.y = self.FLOOR - self.r
        else:
            self.vy -= G
        super().move()
        self.live -= 1
        self.death_check()

    def draw(self):
        pygame.draw.circle(self.screen, BLACK, (self.x - self.vx * 0.25, self.y + self.vy * 0.25), self.r)
        super().draw()


class Cannonball(Bullet):

    def hit_reaction(self):
        self.live = 0


class Laser(Bullet):

    def __init__(self, bullet_gun, surface=screen):
        super().__init__(bullet_gun, surface)
        self.x = bullet_gun.x + (HEIGHT + WIDTH) * math.cos(bullet_gun.an)
        self.y = bullet_gun.y + (HEIGHT + WIDTH) * math.sin(bullet_gun.an)
        self.live = 5
        self.gun = bullet_gun
        self.color = RED
        self.surface = surface

    def draw(self):
        if not self.death_check():
            pygame.draw.line(screen, self.color, (self.x, self.y), (self.gun.x, self.gun.y), 10)
            pygame.draw.circle(screen, self.color, (self.gun.x, self.gun.y), 7)

    def move(self):
        self.live -= 1

    def hit_test(self, circle):
        if circle.x != self.gun.x:
            angle = math.atan((circle.y - self.gun.y) / (circle.x - self.gun.x))
        else:
            angle = math.pi / 2
        if ((abs(math.sin(self.gun.an - angle)) * ((circle.x - self.gun.x) ** 2 + (circle.y - self.gun.y) ** 2) ** 0.5
             <= circle.r) and not self.death_check()):
            return True
        else:
            return False


class Bomb(Bullet):

    def __init__(self, bullet_gun, surface=screen):
        super().__init__(bullet_gun, surface)
        self.vx = self.vy = 0
        self.boom = False

    def move(self):
        if not self.boom:
            super().move()
            if self.y >= HEIGHT - self.r:
                if self.live > 10:
                    self.hit_reaction()
        else:
            self.live -= 1
            self.death_check()

    def hit_reaction(self):
        if self.live > 10:
            self.live = 10
            self.vx = self.vy = 0
            self.r = 50
            self.boom = True


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
        self.death_check()

    def move(self):
        """перемещение целей"""
        super().move()
        if self.y <= self.r:
            self.vy = -abs(self.vy)
            self.y = self.r


class Shar(Target):

    def __init__(self, surface=screen):
        super().__init__(surface)
        self.r = rnd(20, 40)
        self.y = HEIGHT + self.r
        self.vx = 0
        self.vy = rnd(2, 5)
        self.x = rnd(self.r, WIDTH - self.r)

    def draw(self):
        super().draw()
        if self.r != 0:
            shar_texture(self.x, self.y, self.r)


class Airship(Target):

    def __init__(self, surface=screen):
        super().__init__(surface)
        self.r = rnd(15, 30)
        self.x = WIDTH + self.r
        self.vy = 0
        self.vx = - rnd(2, 5)
        self.y = rnd(self.r, HEIGHT - self.r)
        self.circles = [Circle(self.x, self.y + self.r * 4, self.r * 5),
                        Circle(self.x, self.y - self.r * 4, self.r * 5)]

    def draw(self):
        super().draw()
        if self.r != 0:
            airship_texture(self.x, self.y, self.r, self.vx)

    def move(self):
        super().move()
        self.circles = [Circle(self.x, self.y + self.r * 4, self.r * 5),
                        Circle(self.x, self.y - self.r * 4, self.r * 5)]


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


def draw_ellipse_in_rect(ellipse_rect, ellipse_color, shape_rect, ellipse_width=0):
    """нужна для прорисовки секторов эллипса"""
    shape = pygame.surface.Surface(shape_rect[2:4], pygame.SRCALPHA)
    pygame.draw.ellipse(shape, ellipse_color,
                        [ellipse_rect[0] - shape_rect[0], ellipse_rect[1] - shape_rect[1]] + ellipse_rect[2, 4],
                        ellipse_width)
    screen.blit(shape, shape_rect[0:2])


def draw_circle_in_rect(circle_center, r, circle_color, shape_rect, circle_width=0):
    """нужна для прорисовки сектора круга"""
    shape = pygame.Surface(shape_rect[2:4], pygame.SRCALPHA)
    pygame.draw.circle(shape, circle_color, (circle_center[0] - shape_rect[0], circle_center[1] - shape_rect[1]),
                       r, circle_width)
    screen.blit(shape, shape_rect[0:2])


def shar_texture(x, y, r, color_basket=GREY):
    """рисует поверх круга воздушный шар"""
    r_dug = round(r * 4 / (5 ** 0.5))
    gran = round(r * 0.8)

    draw_circle_in_rect((x + r, y), r_dug, BLACK, (x - r, y - gran, r * 2, gran * 2), 1)
    draw_circle_in_rect((x - r, y), r_dug, BLACK, (x - r, y - gran, r * 2, gran * 2), 1)
    draw_circle_in_rect((x, y + r), r_dug, BLACK, (x - gran, y - r, gran * 2, r * 2), 1)

    pygame.draw.line(screen, BLACK, (x - r, y), (x + r, y))
    pygame.draw.line(screen, BLACK, (x, y - r), (x, y + round(r * 1.6)))

    pygame.draw.line(screen, BLACK, (x - round(r * 0.6), y + round(r * 0.8)),
                     (x - round(r * 0.2), y + round(r * 1.6)))
    pygame.draw.line(screen, BLACK, (x + round(r * 0.6), y + round(r * 0.8)),
                     (x + round(r * 0.2), y + round(r * 1.6)))

    pygame.draw.rect(screen, color_basket, (x - round(r * 0.2), y + round(r * 1.6), round(r * 0.4), round(r * 0.3)))


def airship_texture(x, y, r, speed, color=RED, color_basket=GREY):
    """рисует поверх круга дирижабль"""
    r_dug = r * 5
    prop_x = x - 3 * r + 6 * r * int(speed < 0)
    draw_circle_in_rect((x, y - round(r * 3.5)), r_dug, color_basket, (x - r * 2, y, r * 4, r * 2))
    draw_circle_in_rect((x, y - round(r * 3.5)), r_dug, BLACK, (x - r * 2, y, r * 4, r * 2), 1)

    draw_circle_in_rect((x, y + r * 4), r_dug, color, (x - r * 3, y - r, r * 6, r))
    draw_circle_in_rect((x, y - r * 4), r_dug, color, (x - r * 3, y, r * 6, r))

    draw_circle_in_rect((x, y + r * 4), r_dug, BLACK, (x - r * 3, y - r, r * 6, r), 1)
    draw_circle_in_rect((x, y - r * 4), r_dug, BLACK, (x - r * 3, y, r * 6, r), 1)

    pygame.draw.circle(screen, BLACK, (x, y), r, 1)
    pygame.draw.line(screen, BLACK, (x, y - r), (x, y + r))

    draw_circle_in_rect((x, y + r * 4), r_dug, BLACK, (x + r * 2 - r * 5 * int(speed > 0), y - r, r, r))
    draw_circle_in_rect((x, y - r * 4), r_dug, BLACK, (x + r * 2 - r * 5 * int(speed > 0), y, r, r))

    pygame.draw.line(screen, BLACK, (prop_x, y - round(r * 0.5)), (prop_x, y + round(r * 0.5)))


def parachute_texture(x, y, r, color1=YELLOW, color2=CYAN, color_basket=RED):
    """рисует парашют по входным данным"""
    draw_circle_in_rect((x, y), r, color2, (x - r, y - r, 2 * r, round(r * 0.4)))
    draw_circle_in_rect((x, y), r, color1, (x - r, y - r, 2 * r, round(r * 0.2)))
    draw_circle_in_rect((x, y - round(r * 1.6)), r, color1, (x - r, y - round(r * 0.8), 2 * r, r))
    draw_circle_in_rect((x, y - round(r * 5 / 3)), round(r * 4 / 3), color2, (x - r, y - round(r * 0.6), 2 * r, r))

    pygame.draw.line(screen, BLACK, (x - round(r * 0.8), y - round(r * 0.6)), (x - round(r * 0.2), y + round(r * 0.4)))
    pygame.draw.line(screen, BLACK, (x + round(r * 0.8), y - round(r * 0.6)), (x + round(r * 0.2), y + round(r * 0.4)))
    pygame.draw.line(screen, BLACK, (x, y - round(r / 3)), (x, y + round(r * 0.4)))

    pygame.draw.rect(screen, color_basket, (x - round(r * 0.2), y + round(r * 0.4), round(r * 0.4), round(r * 0.8 / 3)))


bullet = 0

clock = pygame.time.Clock()
gun = Gun(screen)
targets = []
for i in range(target_number):
    targets += [Shar()]
finished = False
stop_time = 0
live_sum = True

while not finished:
    # прорисовка основных объектов
    screen.fill(WHITE)
    gun.move()
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
            if event.button == 1:
                if gun.possibility_check():
                    gun.fire2_start()
            elif event.button == 3:
                gun.move_start()
            elif event.button == 2:
                if isinstance(gun, Bomber):
                    gun = Gun(screen, gun.x, gun.y)
                else:
                    gun = Bomber(screen, gun.x, gun.y)
            elif event.button == 5:
                gun = LaserGun(screen, gun.x, gun.y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                gun.fire2_end()
                bullet += 1
            else:
                gun.move_end()
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
                    hit = True
                    for c in t.circles:
                        if not b.hit_test(c):
                            hit = False
                    if hit:
                        t.hit()
                        b.hit_reaction()
    for t in targets:
        t.move()

    # когда кончились мишени, нужно обработать конец игрового сеанса
    if not live_sum:
        stop_time = 90
        live_sum = True
        target_number += 1
        Bullet.bullets = []

    if stop_time > 0:
        draw_number_bullet()
        stop_time -= 1
        if stop_time <= 0:
            targets = []
            for i in range(target_number):
                if rnd(0, 1):
                    targets += [Shar()]
                else:
                    targets += [Airship()]
            bullet = 0

    gun.power_up()
    draw_score()
    pygame.display.update()

pygame.quit()
