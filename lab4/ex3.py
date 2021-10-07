import pygame
import numpy as np


def window(x_w_start, y_w_start, x_w_finish, y_w_finish, x_w_center, y_w_center):
    """
    Рисует окно с заданными координатами.
    :param x_w_start: x координата начальной точки
    :param y_w_start: y координата начальной точки
    :param x_w_finish: x координата конечной точки
    :param y_w_finish: y координата конечной точки
    :param x_w_center: x координата центральной части рамы
    :param y_w_center: y координата центральной части рамы
    """

    pygame.draw.rect(screen, (255, 255, 255), (x_w_start, y_w_start, x_w_finish - x_w_start, y_w_finish - y_w_start))
    pygame.draw.rect(screen, (0, 255, 255),
                     (x_w_start + 10, y_w_start + 10, x_w_finish - x_w_start - 20, y_w_finish - y_w_start - 20))
    pygame.draw.line(screen, (255, 255, 255), (x_w_center, y_w_start + 5), (x_w_center, y_w_finish - 5), 10)
    pygame.draw.line(screen, (255, 255, 255), (x_w_start + 5, y_w_center), (x_w_finish - 5, y_w_center), 10)


def tale(size, direction, center, color):
    """
    рисует хвост кота по его координатам.
    :param size: размер кота
    :param direction: напрвление кота
    :param center: координаты кота
    :param color: цвет кота
    :return:
    """
    tale_a = []
    tale_b = []
    tale_c = []
    tale_d = []
    x_start = center[0] + direction * size * 35
    y_start = center[1] + 15 * size
    pygame.draw.circle(screen, (0, 0, 0), (x_start + direction * 35 * size, y_start + 17.5 * size), 2.5 * size)

    for h_x in range(20 * size):
        tale_a += [[x_start + direction * h_x,
                    y_start - (400 * size ** 2 - h_x ** 2) ** 0.5]]
        tale_b += [[x_start + direction * (h_x * 3 / 4 + 20 * size),
                    y_start + (225 * size ** 2 - (15 * size - h_x * 3 / 4) ** 2) ** 0.5]]
        tale_c += [[x_start + direction * (- h_x + 35 * size),
                    y_start + (400 * size ** 2 - h_x ** 2) ** 0.5]]
        tale_d += [[x_start + direction * (- h_x * 3 / 4 + 15 * size),
                    y_start - (225 * size ** 2 - (15 * size - h_x * 3 / 4) ** 2) ** 0.5]]
    full_tale = tale_a + tale_b + tale_c + tale_d
    pygame.draw.polygon(screen, color, full_tale)
    pygame.draw.polygon(screen, (0, 0, 0), full_tale, 2)
    pygame.draw.circle(screen, color,
                       (x_start + direction * 35 * size, y_start + 17.5 * size), 2.5 * size - 2)


def body(size, center, color):
    """
    рисует тело кота по его координатам
    :param size: размер кота
    :param center: координаты кота
    :param color: цвет кота
    :return:
    """
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (center[0] - size * 40 - 2, center[1] - size * 20 - 2,
                         size * 80 + 4, size * 40 + 4))
    pygame.draw.ellipse(screen, color,
                        (center[0] - size * 40, center[1] - size * 20,
                         size * 80, size * 40))


def first_paws(size, direction, center, color):
    """
    рисует передние лапы кота по его координатам
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param color: цвет кота
    :return:
    """
    pygame.draw.ellipse(screen, color,
                        (center[0] - direction * 30 * size - 10 * size, center[1] + 12 * size, 20 * size, 10 * size))
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (center[0] - direction * 30 * size - 10 * size, center[1] + 12 * size, 20 * size, 10 * size), 2)
    pygame.draw.ellipse(screen, color,
                        (center[0] - direction * 42 * size - 5 * size, center[1] - 5 * size, 10 * size, 18 * size))
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (center[0] - direction * 42 * size - 5 * size, center[1] - 5 * size, 10 * size, 18 * size), 2)


def second_paws(size, direction, center, color):
    """
    рисует задние лапы кота по его координатам
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param color: цвет кота
    :return:
    """
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (center[0] + direction * size * 27 - size * 12 - 2, center[1] - size * 2 - 2,
                         size * 24 + 4, size * 24 + 4))
    pygame.draw.ellipse(screen, color,
                        (center[0] + direction * size * 27 - size * 12, center[1] - size * 2,
                         size * 24, size * 24))
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (center[0] + direction * size * 39 - size * 4 - 2, center[1] + size * 12 - 2,
                         size * 8 + 4, size * 20 + 4))
    pygame.draw.ellipse(screen, color,
                        (center[0] + direction * size * 39 - size * 4, center[1] + size * 12,
                         size * 8, size * 20))


def head_main(size, direction, center, color):
    """
    рисует основу головы кота
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param color: цвет кота
    :return:
    """
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (center[0] - direction * size * 35 - size * 16 - 2, center[1] - size * 19 - 2,
                         size * 32 + 4, size * 28 + 4))
    pygame.draw.ellipse(screen, color,
                        (center[0] - direction * size * 35 - size * 16, center[1] - size * 19,
                         size * 32, size * 28))


def head_ears(size, direction, center, color):
    """
    рисует уши кота по его координатам
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param color: цвет кота
    :return:
    """
    pygame.draw.polygon(screen, color, [[center[0] - direction * size * 48, center[1] - size * 12],
                                        [center[0] - direction * size * 49, center[1] - size * 19],
                                        [center[0] - direction * size * 43, center[1] - size * 15]])
    pygame.draw.polygon(screen, (0, 0, 0), [[center[0] - direction * size * 48, center[1] - size * 12],
                                            [center[0] - direction * size * 49, center[1] - size * 19],
                                            [center[0] - direction * size * 43, center[1] - size * 15]], 2)
    pygame.draw.polygon(screen, ((color[0] + 255) // 2, (color[1] + 255) // 2, (color[2] + 255) // 2),
                        [[center[0] - direction * size * 47, center[1] - size * 14],
                         [center[0] - direction * size * 47.6, center[1] - size * 17],
                         [center[0] - direction * size * 45, center[1] - size * 15]])
    pygame.draw.polygon(screen, (0, 0, 0), [[center[0] - direction * size * 47, center[1] - size * 14],
                                            [center[0] - direction * size * 47.6, center[1] - size * 17],
                                            [center[0] - direction * size * 45, center[1] - size * 15]], 2)
    pygame.draw.polygon(screen, color, [[center[0] - direction * size * 21, center[1] - size * 9],
                                        [center[0] - direction * size * 19.7, center[1] - size * 16],
                                        [center[0] - direction * size * 26, center[1] - size * 12.5]])
    pygame.draw.polygon(screen, (0, 0, 0), [[center[0] - direction * size * 21, center[1] - size * 9],
                                            [center[0] - direction * size * 19.7, center[1] - size * 16],
                                            [center[0] - direction * size * 26, center[1] - size * 12.5]], 2)
    pygame.draw.polygon(screen, ((color[0] + 255) // 2, (color[1] + 255) // 2, (color[2] + 255) // 2),
                        [[center[0] - direction * size * 22, center[1] - size * 11],
                         [center[0] - direction * size * 21.2, center[1] - size * 14],
                         [center[0] - direction * size * 24, center[1] - size * 12.6]])
    pygame.draw.polygon(screen, (0, 0, 0), [[center[0] - direction * size * 22, center[1] - size * 11],
                                            [center[0] - direction * size * 21.2, center[1] - size * 14],
                                            [center[0] - direction * size * 24, center[1] - size * 12.6]], 2)


def head_nose(size, direction, center, color):
    """
    рисует нос кота по его координатам
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param color: цвет кота
    :return:
    """
    pygame.draw.polygon(screen, ((color[0] + 255) // 2, (color[1] + 255) // 2, (color[2] + 255) // 2),
                        [[center[0] - direction * size * 36.4, center[1] + size * 2],
                         [center[0] - direction * size * 38, center[1] + size * 0.4],
                         [center[0] - direction * size * 34, center[1] + size * 1]])
    pygame.draw.polygon(screen, (0, 0, 0),
                        [[center[0] - direction * size * 36.4, center[1] + size * 2],
                         [center[0] - direction * size * 38, center[1] + size * 0.4],
                         [center[0] - direction * size * 34, center[1] + size * 1]], 2)
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 36.4, center[1] + size * 2),
                     (center[0] - direction * size * 37, center[1] + size * 6), 2)
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 37, center[1] + size * 6),
                     (center[0] - direction * size * 38.3, center[1] + size * 6.6), 2)
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 37, center[1] + size * 6),
                     (center[0] - direction * size * 36, center[1] + size * 7), 2)


def head_eye_pupil(size, direction, center, dislocation):
    """
    рисует зрачок по координатам кота
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param dislocation: отклонение
    :return:
    """
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (center[0] - direction * size * (dislocation[0] - 1) - size * 0.5,
                         center[1] - size * (dislocation[1] - 1.6), size, 4.8 * size))


def head_eye(size, direction, center, eye_color, dislocation):
    """

    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param eye_color: цвет глаз
    :param dislocation: отклонение
    :return:
    """
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (center[0] - direction * size * dislocation[0] - size * 3, center[1] - size * dislocation[1],
                         6 * size, 8 * size))
    pygame.draw.ellipse(screen, eye_color,
                        (center[0] - direction * size * dislocation[0] - size * 3 + 2,
                         center[1] - size * dislocation[1] + 2, 6 * size - 4, 8 * size - 4))
    head_eye_pupil(size, direction, center, dislocation)


def head_eyes(size, direction, center, eye_color):
    """
    объединяет глаза кота с их зрачками
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param eye_color: цвет глаз
    :return:
    """
    head_eye(size, direction, center, eye_color, (41, 9.6))
    head_eye(size, direction, center, eye_color, (29, 8.6))


def head_mustache(size, direction, center):
    """
    рисует усы кота по его координатам
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :return:
    """
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 39, center[1] - size * 1),
                     (center[0] - direction * size * 50, center[1] - size * 8))
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 39.6, center[1]),
                     (center[0] - direction * size * 55, center[1] - size * 5))
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 38.7, center[1] + size * 1.3),
                     (center[0] - direction * size * 53, center[1] + size * 1.6))
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 33, center[1]),
                     (center[0] - direction * size * 20, center[1] - size * 5))
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 32.4, center[1] + size),
                     (center[0] - direction * size * 15, center[1] - size * 1))
    pygame.draw.line(screen, (0, 0, 0), (center[0] - direction * size * 33, center[1] + size * 2.3),
                     (center[0] - direction * size * 17, center[1] + size * 3.6))


def head(size, direction, center, color, eye_color):
    """
    объединяет результаты всех функций рисования головы
    :param size: размер кота
    :param direction: направление кота
    :param center: координаты кота
    :param color: цвет кота
    :param eye_color: цвет глаз кота
    :return:
    """
    head_main(size, direction, center, color)
    head_ears(size, direction, center, color)
    head_nose(size, direction, center, color)
    head_eyes(size, direction, center, eye_color)
    head_mustache(size, direction, center)


def cat(size, direction, center, color, eye_color):
    """
    объединяет результаты всех функций рисования кота
    :param size:
    :param direction:
    :param center:
    :param color:
    :param eye_color:
    :return:
    """
    tale(size, direction, center, color)
    body(size, center, color)
    first_paws(size, direction, center, color)
    second_paws(size, direction, center, color)
    head(size, direction, center, color, eye_color)


def klubok(k_size, k_x, k_y, k_left):
    for i in range(100):
        pygame.draw.line(screen, (0, 0, 0),
                         (k_x - k_left * k_size * 0.25 * (i - 1), k_y + k_size * 5 * (1 + np.sin(i / 20))),
                         (k_x - k_left * k_size * 0.25 * i, k_y + k_size * 5 * (1 + np.sin(i / 20))), 1)
    pygame.draw.circle(screen, (150, 150, 150), (k_x, k_y), k_size * 10)
    pygame.draw.circle(screen, (0, 0, 0), (k_x, k_y), k_size * 8, 2)
    pygame.draw.circle(screen, (150, 150, 150), (k_x - k_left * 3, k_y + 3), k_size * 8 + k_left * 1)
    pygame.draw.circle(screen, (0, 0, 0), (k_x - k_left * 2, k_y + 2), k_size * 6, 2)
    pygame.draw.circle(screen, (150, 150, 150), (k_x - k_left * 4, k_y + 4), k_size * 6 + 1)
    pygame.draw.circle(screen, (0, 0, 0), (k_x - k_left * 4, k_y + 4), k_size * 4, 2)
    pygame.draw.circle(screen, (150, 150, 150), (k_x - k_left * 6, k_y + 6), k_size * 4 + 1)
    pygame.draw.circle(screen, (0, 0, 0), (k_x, k_y), k_size * 10, 2)
    pygame.draw.line(screen, (0, 0, 0), (k_x - k_left * k_size * 0.4, k_y + k_size * 3),
                     (k_x - k_left * k_size * 2, k_y + k_size * 7), 2)
    pygame.draw.line(screen, (0, 0, 0), (k_x - k_left * k_size * 3, k_y - k_size * 0.3),
                     (k_x - k_left * k_size * 6, k_y + k_size * 1), 2)
    pygame.draw.line(screen, (0, 0, 0), (k_x - k_left * k_size * 2, k_y + k_size * 2),
                     (k_x - k_left * k_size * 5, k_y + k_size * 5), 2)


FPS = 30
finished = False
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 700))
# начало рисования
pygame.draw.rect(screen, (75, 50, 0), (0, 0, 600, 350))
pygame.draw.rect(screen, (145, 130, 0), (0, 350, 600, 350))
window(300, 50, 500, 300, 400, 150)
cat(3, 1, (500, 450), (255, 130, 0), (0, 255, 0))
klubok(3, 400, 600, 1)
window(50, 50, 250, 300, 150, 150)
cat(2, -1, (150, 600), (100, 100, 100), (0, 255, 255))
cat(1, 1, (67, 400), (200, 200, 200), (100, 0, 200))
klubok(2, 200, 437, -1)
klubok(7, 50, 500, 1)
cat(3, -1, (550, 600), (255, 255, 255), (100, 100, 100))
cat(2, 1, (300, 470), (50, 50, 50), (200, 200, 200))
window(550, 50, 750, 300, 650, 150)
pygame.display.update()

# ожидание закрытия окна
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
