import pygame

FPS = 30
finished = False
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))
# создание фона
pygame.draw.rect(screen, (200, 200, 200), (0, 0, 600, 600))
# тело смайлика
pygame.draw.circle(screen, (255, 255, 0), (300, 300), 200)
pygame.draw.circle(screen, (0, 0, 0), (300, 300), 200, 2)
# левый, правый глаза
pygame.draw.circle(screen, (255, 0, 0), (215, 240), 33)
pygame.draw.circle(screen, (0, 0, 0), (215, 240), 33, 2)
pygame.draw.circle(screen, (0, 0, 0), (215, 240), 16)
pygame.draw.circle(screen, (255, 0, 0), (385, 240), 30)
pygame.draw.circle(screen, (0, 0, 0), (385, 240), 30, 2)
pygame.draw.circle(screen, (0, 0, 0), (385, 240), 14)
# брови
pygame.draw.line(screen, (0, 0, 0), (130, 140), (260, 240), 15)
pygame.draw.line(screen, (0, 0, 0), (450, 120), (340, 250), 15)
# рот
pygame.draw.rect(screen, (0, 0, 0), (200, 390, 200, 30))
pygame.display.update()
# ожидание закрытия окна
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
pygame.quit()
