import pygame
import numpy as np


def window(x_w_start, y_w_start, x_w_finish, y_w_finish, x_w_center, y_w_center):
    pygame.draw.rect(screen, (255, 255, 255), (x_w_start, y_w_start, x_w_finish - x_w_start, y_w_finish - y_w_start))
    pygame.draw.rect(screen, (0, 255, 255),
                     (x_w_start + 10, y_w_start + 10, x_w_finish - x_w_start - 20, y_w_finish - y_w_start - 20))
    pygame.draw.line(screen, (255, 255, 255), (x_w_center, y_w_start + 5), (x_w_center, y_w_finish - 5), 10)
    pygame.draw.line(screen, (255, 255, 255), (x_w_start + 5, y_w_center), (x_w_finish - 5, y_w_center), 10)


def cat(size, left, x_center, y_center, color_r, color_g, color_b, eye_color_r, eye_color_g, eye_color_b):
    # хвост
    tale_a = []
    tale_b = []
    tale_c = []
    tale_d = []
    x_start = x_center + left * size * 35
    y_start = y_center + 15 * size
    pygame.draw.circle(screen, (0, 0, 0), (x_start + left * 35 * size, y_start + 17.5 * size), 2.5 * size)
    for h_x in range(20 * size):
        tale_a += [[x_start + left * h_x,
                    y_start - (400 * size ** 2 - h_x ** 2) ** 0.5]]
        tale_b += [[x_start + left * (h_x * 3 / 4 + 20 * size),
                    y_start + (225 * size ** 2 - (15 * size - h_x * 3 / 4) ** 2) ** 0.5]]
        tale_c += [[x_start + left * (- h_x + 35 * size),
                    y_start + (400 * size ** 2 - h_x ** 2) ** 0.5]]
        tale_d += [[x_start + left * (- h_x * 3 / 4 + 15 * size),
                    y_start - (225 * size ** 2 - (15 * size - h_x * 3 / 4) ** 2) ** 0.5]]
    pygame.draw.polygon(screen, (color_r, color_g, color_b), tale_a + tale_b + tale_c + tale_d)
    pygame.draw.polygon(screen, (0, 0, 0), tale_a + tale_b + tale_c + tale_d, 2)
    pygame.draw.circle(screen, (color_r, color_g, color_b),
                       (x_start + left * 35 * size, y_start + 17.5 * size), 2.5 * size - 2)
    # тело
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center - size * 40 - 2, y_center - size * 20 - 2,
                         size * 80 + 4, size * 40 + 4))
    pygame.draw.ellipse(screen, (color_r, color_g, color_b),
                        (x_center - size * 40, y_center - size * 20,
                         size * 80, size * 40))
    # передние_лапы
    pygame.draw.ellipse(screen, (color_r, color_g, color_b),
                        (x_center - left * 30 * size - 10 * size, y_center + 12 * size, 20 * size, 10 * size))
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center - left * 30 * size - 10 * size, y_center + 12 * size, 20 * size, 10 * size), 2)
    pygame.draw.ellipse(screen, (color_r, color_g, color_b),
                        (x_center - left * 42 * size - 5 * size, y_center - 5 * size, 10 * size, 18 * size))
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center - left * 42 * size - 5 * size, y_center - 5 * size, 10 * size, 18 * size), 2)
    # задняя_лапа
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center + left * size * 27 - size * 12 - 2, y_center - size * 2 - 2,
                         size * 24 + 4, size * 24 + 4))
    pygame.draw.ellipse(screen, (color_r, color_g, color_b),
                        (x_center + left * size * 27 - size * 12, y_center - size * 2,
                         size * 24, size * 24))
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center + left * size * 39 - size * 4 - 2, y_center + size * 12 - 2,
                         size * 8 + 4, size * 20 + 4))
    pygame.draw.ellipse(screen, (color_r, color_g, color_b),
                        (x_center + left * size * 39 - size * 4, y_center + size * 12,
                         size * 8, size * 20))
    # голова_основа
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center - left * size * 35 - size * 16 - 2, y_center - size * 19 - 2,
                         size * 32 + 4, size * 28 + 4))
    pygame.draw.ellipse(screen, (color_r, color_g, color_b),
                        (x_center - left * size * 35 - size * 16, y_center - size * 19,
                         size * 32, size * 28))
    # голова_уши
    pygame.draw.polygon(screen, (color_r, color_g, color_b), [[x_center - left * size * 48, y_center - size * 12],
                                                              [x_center - left * size * 49, y_center - size * 19],
                                                              [x_center - left * size * 43, y_center - size * 15]])
    pygame.draw.polygon(screen, (0, 0, 0), [[x_center - left * size * 48, y_center - size * 12],
                                            [x_center - left * size * 49, y_center - size * 19],
                                            [x_center - left * size * 43, y_center - size * 15]], 2)
    pygame.draw.polygon(screen, ((color_r + 255) // 2, (color_g + 255) // 2, (color_b + 255) // 2),
                        [[x_center - left * size * 47, y_center - size * 14],
                         [x_center - left * size * 47.6, y_center - size * 17],
                         [x_center - left * size * 45, y_center - size * 15]])
    pygame.draw.polygon(screen, (0, 0, 0), [[x_center - left * size * 47, y_center - size * 14],
                                            [x_center - left * size * 47.6, y_center - size * 17],
                                            [x_center - left * size * 45, y_center - size * 15]], 2)
    pygame.draw.polygon(screen, (color_r, color_g, color_b), [[x_center - left * size * 21, y_center - size * 9],
                                                              [x_center - left * size * 19.7, y_center - size * 16],
                                                              [x_center - left * size * 26, y_center - size * 12.5]])
    pygame.draw.polygon(screen, (0, 0, 0), [[x_center - left * size * 21, y_center - size * 9],
                                            [x_center - left * size * 19.7, y_center - size * 16],
                                            [x_center - left * size * 26, y_center - size * 12.5]], 2)
    pygame.draw.polygon(screen, ((color_r + 255) // 2, (color_g + 255) // 2, (color_b + 255) // 2),
                        [[x_center - left * size * 22, y_center - size * 11],
                         [x_center - left * size * 21.2, y_center - size * 14],
                         [x_center - left * size * 24, y_center - size * 12.6]])
    pygame.draw.polygon(screen, (0, 0, 0), [[x_center - left * size * 22, y_center - size * 11],
                                            [x_center - left * size * 21.2, y_center - size * 14],
                                            [x_center - left * size * 24, y_center - size * 12.6]], 2)
    # голова_нос
    pygame.draw.polygon(screen, ((color_r + 255) // 2, (color_g + 255) // 2, (color_b + 255) // 2),
                        [[x_center - left * size * 36.4, y_center + size * 2],
                         [x_center - left * size * 38, y_center + size * 0.4],
                         [x_center - left * size * 34, y_center + size * 1]])
    pygame.draw.polygon(screen, (0, 0, 0),
                        [[x_center - left * size * 36.4, y_center + size * 2],
                         [x_center - left * size * 38, y_center + size * 0.4],
                         [x_center - left * size * 34, y_center + size * 1]], 2)
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 36.4, y_center + size * 2),
                     (x_center - left * size * 37, y_center + size * 6), 2)
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 37, y_center + size * 6),
                     (x_center - left * size * 38.3, y_center + size * 6.6), 2)
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 37, y_center + size * 6),
                     (x_center - left * size * 36, y_center + size * 7), 2)
    # голова_глаза
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center - left * size * 41 - size * 3, y_center - size * 9.6, 6 * size, 8 * size))
    pygame.draw.ellipse(screen, (eye_color_r, eye_color_g, eye_color_b),
                        (x_center - left * size * 41 - size * 3 + 2,
                         y_center - size * 9.6 + 2, 6 * size - 4, 8 * size - 4))
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center - left * size * 29 - size * 3, y_center - size * 8.6, 6 * size, 8 * size))
    pygame.draw.ellipse(screen, (eye_color_r, eye_color_g, eye_color_b),
                        (x_center - left * size * 29 - size * 3 + 2,
                         y_center - size * 8.6 + 2, 6 * size - 4, 8 * size - 4))
    # голова_глаза_зрачки
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center - left * size * 28 - size * 0.5, y_center - size * 7, size, 4.8 * size))
    pygame.draw.ellipse(screen, (0, 0, 0),
                        (x_center - left * size * 40 - size * 0.5, y_center - size * 8, size, 4.8 * size))
    # голова_усы
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 39, y_center - size * 1),
                     (x_center - left * size * 50, y_center - size * 8))
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 39.6, y_center),
                     (x_center - left * size * 55, y_center - size * 5))
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 38.7, y_center + size * 1.3),
                     (x_center - left * size * 53, y_center + size * 1.6))
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 33, y_center),
                     (x_center - left * size * 20, y_center - size * 5))
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 32.4, y_center + size),
                     (x_center - left * size * 15, y_center - size * 1))
    pygame.draw.line(screen, (0, 0, 0), (x_center - left * size * 33, y_center + size * 2.3),
                     (x_center - left * size * 17, y_center + size * 3.6))


def klubok(k_size, k_x, k_y, k_left):
    for i in range(100):
        pygame.draw.line(screen, (0, 0, 0), (k_x - k_left * k_size * 0.25 * (i-1), k_y + k_size * 5 * (1 + np.sin(i/20))),
                        (k_x - k_left * k_size * 0.25 * i, k_y + k_size * 5 * (1 + np.sin(i/20))), 1)
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
cat(3, 1, 500, 450, 255, 130, 0, 0, 255, 0)
klubok(3, 400, 600, 1)
window(50, 50, 250, 300, 150, 150)
cat(2, -1, 150, 600, 100, 100, 100, 0, 255, 255)
cat(1, 1, 67, 400, 200, 200, 200, 100, 0, 200)
klubok(2, 200, 437, -1)
klubok(7, 50, 500, 1)
cat(3, -1, 550, 600, 255, 255, 255, 100, 100, 100)
cat(2, 1, 300, 470, 50, 50, 50, 200, 200, 200)
window(550, 50, 750, 300, 650, 150)
pygame.display.update()
# ожидание закрытия окна
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
