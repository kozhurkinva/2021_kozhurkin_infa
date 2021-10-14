from random import randint
import pygame

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))
font = pygame.font.Font(None, 100)
score_pos = (10, 10)
game_time_pos = (1115, 10)
new_game_button_rect = [500, 600, 200, 100]

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, BLACK]

DEATH_TIME = 100
BALLS_NUMBER = 5
GAME_START_TIME = 1800
GAME_TEXT = pygame.font.Font(None, 50).render("GAME", False, BLACK)
NEW_TEXT = pygame.font.Font(None, 50).render("NEW", False, BLACK)
TOP_SCORE_TEXT = pygame.font.Font(None, 100).render("TOP SCORE", False, WHITE)
YOU_TEXT = pygame.font.Font(None, 100).render("YOU", False, WHITE)


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

    def click(self, click_pos):
        """
        проверка на клик по объекту Ball, возвращает изменение счёта и новый (или старый) обЪект Ball
        :param click_pos: позиция клика
        :return: изменение счёта, новый (или старый) объект Ball
        """
        if (self.x - click_pos[0]) ** 2 + (self.y - click_pos[1]) ** 2 <= self.r ** 2:
            if self.strange == 0:
                return 3, Ball()
            else:
                self.strange += 1
                self.color += [randint(0, 4)]
                if self.color[-1] == self.color[-2]:
                    self.color[-1] = 5
                self.time += 1
                return 1, self
        else:
            return 0, self


def draw_new_game_button():
    """
    рисует кнопку новой игры
    """
    delta_x, delta_y = 30, 10
    pygame.draw.rect(screen, WHITE, new_game_button_rect)
    screen.blit(NEW_TEXT, (new_game_button_rect[0] + delta_x, new_game_button_rect[1] + delta_y))
    screen.blit(GAME_TEXT, (new_game_button_rect[0] - delta_x + new_game_button_rect[2] // 2,
                            new_game_button_rect[1] + delta_y + new_game_button_rect[3] // 2))


def draw_top_score():
    """
    рисует таблицу лучших результатов
    """
    x_number, x_score = 250, 700
    y_start = 100
    delta_top_x = 150
    delta_top_y = 50
    screen.blit(TOP_SCORE_TEXT, (375, 10))
    with open("top_score.txt") as tops:
        top_score = tops.read().split()
        for i in range(10):
            top_number_text = font.render(str(i + 1), False, WHITE)
            top_score_text = font.render(str(top_score[i]), False, WHITE)
            texts = [[top_score_text, x_score], [top_number_text, x_number]]
            for text in texts:
                screen.blit(text[0], ((i % 2) * delta_top_x + text[1], y_start + i * delta_top_y))


def check_tops():
    """
    проверяет результат на попадение в таблицу лучших, также меняет её
    :return: позизия в таблице (от 0 до 9)
    """
    with open("top_score.txt") as tops:
        top_scores = tops.read().split()
        you = 0
        while score <= int(top_scores[you]):
            you += 1
    if you == 10:
        return -10
    else:
        top_scores = top_scores[0:you] + [score] + top_scores[you:9] + [-1]
        with open("top_score.txt", "w") as tops:
            top_scores_text = ""
            for top_score in top_scores:
                top_scores_text += str(top_score) + " "
            tops.write(top_scores_text)
        return you


def draw_you():
    """
    рисует надпись YOU на строчке таблицы рядом с новым результатом (если он попал в таблицу)
    """
    x_start, y_start, delta_top_y = 500, 100, 50
    screen.blit(YOU_TEXT, (x_start, y_start + your_pos * delta_top_y))


def button_click(event, button):
    """
    проверка на нажатие по кнопке
    :param event: массив с координатами клика
    :param button: массив с координатами и размерами кнопки
    :return: True/False, нажатие кнопки
    """
    click = True
    for x_and_y in range(2):
        click *= ((event[x_and_y] <= button[x_and_y] + button[x_and_y + 2])
                  and (event[x_and_y] >= button[x_and_y]))
    return click


def game_texts():
    """
    рисует счёт и оставшееся время в текущей игре
    """
    score_text = font.render(str(score), False, WHITE)
    game_time_text = font.render(str(game_time // 30), False, WHITE)
    screen.blit(score_text, score_pos)
    screen.blit(game_time_text, (game_time_pos[0] + 40 * int(game_time // 10 == 0), game_time_pos[1]))


clock = pygame.time.Clock()
finished, game_over = False, True
game_time = 0
balls = []
score = 0
your_pos = -10
for i in range(BALLS_NUMBER):
    balls += [Ball()]

while not finished:
    clock.tick(FPS)
    for i in range(BALLS_NUMBER):
        for j in range(len(balls[i].color)):
            pygame.draw.circle(screen, COLORS[(balls[i].color[j])], (balls[i].x, balls[i].y),
                               balls[i].r * (len(balls[i].color) - j) // len(balls[i].color))
        balls[i].move()
        balls[i].d_move()
        if randint(0, balls[i].time) >= DEATH_TIME:
            balls[i] = Ball()
    if game_over:
        draw_new_game_button()
        draw_top_score()
        draw_you()
    else:
        game_time -= 1
        game_texts()
    if game_time <= 0:
        game_time = GAME_START_TIME
        game_over = True
        your_pos = check_tops()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                for i in range(BALLS_NUMBER):
                    d_score, balls[i] = balls[i].click(event.pos)
                    score += d_score
            else:
                if button_click([event.pos[0], event.pos[1]], new_game_button_rect):
                    game_over = False
                    score = 0
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
