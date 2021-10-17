from random import randint
import pygame

pygame.init()

FPS = 30
display = (1200, 900)
screen = pygame.display.set_mode(display)
fonts = pygame.font.Font(None, 100), pygame.font.Font(None, 50), pygame.font.Font(None, 1400)
score_pos = (10, 10)
game_time_pos = (1115, 10)
new_game_button_rect = [500, 700, 200, 100]

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

DEATH_TIME = 100
BALLS_NUMBER = 5
GAME_START_TIME = 1800
GAME_TEXT = fonts[1].render("GAME", False, BLACK)
NEW_TEXT = fonts[1].render("NEW", False, BLACK)
TOP_SCORE_TEXT = fonts[0].render("TOP SCORE", False, WHITE)
YOU_TEXT = fonts[0].render("YOU", False, WHITE)
PAUSE_TEXT = fonts[0].render("PAUSE", False, WHITE)


class RectOfDeath(object):
    """
    класс объектов, заканчивающих игру при прикосновении
    """

    def __init__(self, number):
        """
        создание объекта Death_rect
        """
        self.start_time = 100 / number
        self.number = number
        self.time = randint(-300, -150)
        size = [randint(100, 150), randint(100, 150)]
        size[randint(0, 1)] *= 5
        self.rect = [randint(-size[0], display[0]), randint(-size[1], display[1]), size[0], size[1]]
        for n in range(2):
            if self.rect[n] < 0:
                self.rect[n] = 0
            elif self.rect[n] > display[n] - size[n]:
                self.rect[n] = display[n] - size[n]

    def color(self):
        """
        цвет объекта в данный момент
        :return: цвет объекта
        """
        if (self.time <= self.start_time) and (self.time >= 0):
            return gray(100 * (self.start_time - abs(self.start_time - self.time)) // self.start_time)
        elif self.time > self.start_time:
            return WHITE
        else:
            return BLACK

    def death_check(self):
        """
        проверка на прикосновение
        :return: True/False новый game_over
        """
        if self.time > self.start_time:
            pos = pygame.mouse.get_pos()
            if rect_check(pos, self.rect):
                return True
            else:
                return False
        else:
            return False


class Ball(object):
    """
    класс объектов "мишеней"
    """

    def __init__(self):
        """
        создание объекта Ball
        """
        self.clicker = randint(1, 20) // 20
        self.r = randint(10, 100)
        self.x = randint(self.r, display[0] - self.r)
        self.y = randint(self.r, display[1] - self.r)
        self.color = [randint(0, 5)]
        for k in range(self.clicker):
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
        if self.x > display[0] - self.r:
            x_out_screen = 1
        if self.y < self.r:
            y_out_screen = -1
        if self.y > display[1] - self.r:
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
            if self.clicker == 0:
                return 3, Ball()
            else:
                self.clicker += 1
                self.color += [randint(0, 4)]
                if self.color[-1] == self.color[-2]:
                    self.color[-1] = 5
                self.time += 1
                return 1, self
        else:
            return 0, self


def gray(brightness):
    """
    возвращает серый цвет заданной яркости (0 - чёрный, 255 - белый)
    :param brightness: яркость
    :return: серый цвет заданной яркости
    """
    return brightness, brightness, brightness


def rect_check(pos, rect):
    """
    проверяет попадание данных координат в данный прямоугольник
    :param pos: координаты ...
    :param rect: координаты прямоугольника
    :return: True/False попадание в прямоугольник
    """
    checking = True
    for i1 in range(2):
        checking = checking and (pos[i1] >= rect[i1]) and (pos[i1] <= rect[i1] + rect[i1 + 2])
    return checking


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
    y_start = 150
    delta_top_x = 150
    delta_top_y = 50
    screen.blit(TOP_SCORE_TEXT, (375, 60))
    with open("top_score.txt") as tops:
        top_score = tops.read().split()
        for i2 in range(10):
            top_number_text = fonts[0].render(str(i2 + 1), False, WHITE)
            top_score_text = fonts[0].render(str(top_score[i2]), False, WHITE)
            texts = [[top_score_text, x_score], [top_number_text, x_number]]
            for text in texts:
                screen.blit(text[0], ((i2 % 2) * delta_top_x + text[1], y_start + i2 * delta_top_y))


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
    x_start, y_start, delta_top_y = 500, 150, 50
    screen.blit(YOU_TEXT, (x_start, y_start + your_pos * delta_top_y))


def draw_pause():
    """
    рисует надпись "Pause"
    """
    x_start, y_start = 500, 400
    screen.blit(PAUSE_TEXT, (x_start, y_start))


def button_click(click_pos, button):
    """
    проверка на нажатие по кнопке
    :param click_pos: массив с координатами клика
    :param button: массив с координатами и размерами кнопки
    :return: True/False, нажатие кнопки
    """
    click = True
    for x_and_y in range(2):
        click *= ((click_pos[x_and_y] <= button[x_and_y] + button[x_and_y + 2])
                  and (click_pos[x_and_y] >= button[x_and_y]))
    return click


def game_texts():
    """
    рисует счёт и оставшееся время в текущей игре
    """
    score_text = fonts[0].render(str(score), False, WHITE)
    screen.blit(score_text, score_pos)


clock = pygame.time.Clock()
finished, game_over, paused = False, True, False
balls = []
score = 0
your_pos = -10
for i in range(BALLS_NUMBER):
    balls += [Ball()]
death_rectos = [RectOfDeath(1)]
while not finished:
    clock.tick(FPS)
    if not paused:
        paused = not pygame.mouse.get_focused()
        if not game_over:
            for j in range(len(death_rectos)):
                if death_rectos[j].time >= 0:
                    pygame.draw.rect(screen, death_rectos[j].color(), death_rectos[j].rect)
                    game_over = death_rectos[j].death_check()
                    if death_rectos[j].time >= death_rectos[j].start_time + 20:
                        death_rectos += [RectOfDeath(death_rectos[j].number + 1)]
                        death_rectos[j] = RectOfDeath(death_rectos[j].number + 1)
                death_rectos[j].time += 1
            game_texts()
            if game_over:
                your_pos = check_tops()
                death_rectos = [RectOfDeath(1)]
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
    else:
        draw_pause()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                paused = False

pygame.quit()
