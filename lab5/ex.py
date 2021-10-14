from random import randint
import pygame

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))
font = pygame.font.Font(None, 100)
score_pos = (10, 10)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

death_time = 100
number_balls = 5


class Ball(object):
    """
    класс объектов "мишеней"
    """

    def __init__(self):
        """
        создание объекта Ball
        """
        self.strange = randint(1, 20) // 20
        self.r = randint(10, 100)
        self.x = randint(self.r, 1200 - self.r)
        self.y = randint(self.r, 900 - self.r)
        self.color = [randint(0, 5)]
        for k in range(self.strange):
            self.color += [randint(0, 4)]
            if self.color[k + 1] == self.color[k]:
                self.color[k + 1] = 5
        self.speed_x = randint(-10, 10)
        self.speed_y = randint(-10, 10)
        self.time = 0

    def move(self):
        """
        перемещение объекта Ball
        """
        self.x += self.speed_x
        self.y += self.speed_y
        self.time += 1

    def d_move(self):
        """
        изменение скорости объекта Ball (при столкновении)
        """
        x_out_screen = 0
        y_out_screen = 0
        if self.x < self.r:
            x_out_screen = -1
        if self.x > 1200 - self.r:
            x_out_screen = 1
        if self.y < self.r:
            y_out_screen = -1
        if self.y > 900 - self.r:
            y_out_screen = 1
        if x_out_screen ** 2 + y_out_screen ** 2 != 0:
            self.speed_y = randint(-10 + 11 * int(y_out_screen == -1), 10 - 11 * int(y_out_screen == 1))
            self.speed_x = randint(-10 + 11 * int(x_out_screen == -1), 10 - 11 * int(x_out_screen == 1))

    def check(self, click_pos):
        """
        проверка на клик по объекту Ball, возвращает изменение счёта и новый (или старый) обЪект Ball
        :param click_pos: позиция клика
        :return: изменение счёта, новый (или старый) объект Ball
        """
        if (self.x - click_pos[0]) ** 2 + (self.y - click_pos[1]) ** 2 <= self.r ** 2:
            if self.strange == 0:
                return 10, Ball()
            else:
                self.strange += 1
                self.color += [randint(0, 4)]
                if self.color[-1] == self.color[-2]:
                    self.color[-1] = 5
                self.time += 1
                return 1, self
        else:
            return 0, self


pygame.display.update()
clock = pygame.time.Clock()
finished = False
balls = []
score = 0
for i in range(number_balls):
    balls += [Ball()]

while not finished:
    clock.tick(FPS)
    for i in range(len(balls)):
        for j in range(len(balls[i].color)):
            pygame.draw.circle(screen, COLORS[balls[i].color[j]], (balls[i].x, balls[i].y),
                               balls[i].r * (len(balls[i].color) - j) // len(balls[i].color))
        balls[i].move()
        balls[i].d_move()
        if balls[i].time >= death_time:
            balls[i] = Ball()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(balls)):
                d_score, balls[i] = balls[i].check(event.pos)
                score += d_score
    score_text = font.render(str(score), False, WHITE)
    screen.blit(score_text, score_pos)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
