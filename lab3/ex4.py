import turtle as t
import random as rnd


class Dog(object):

    def __init__(self):
        self.me = t.Turtle(shape="circle")
        self.me.shapesize(size)
        self.x = rnd.randint(- a // 2 + 1, a // 2)
        self.y = rnd.randint(- b // 2 + 1, b // 2)
        self.x_speed = rnd.random() * speed - speed / 2
        self.y_speed = rnd.random() * speed - speed / 2
        self.me.penup()
        self.me.speed(0)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.me.goto(self.x, self.y)

    def d_move(self):
        if realism == "y":
            if push > 0:
                self.realistic()
        if (abs(self.x) >= a * 0.5) and (self.x * self.x_speed > 0):
            self.x_speed *= -1
        if (abs(self.y) >= b * 0.5) and (self.y * self.y_speed > 0):
            self.y_speed *= -1
        if realism == "y":
            if push < 0:
                self.realistic()

    def realistic(self):
        for cat in dogs:
            if self != cat:
                dx = self.x - cat.x
                dy = self.y - cat.y
                power = push / (dx ** 2 + dy ** 2) ** 1.5
                self.x_speed += dx * power
                self.y_speed += dy * power


def simulation():
    global dogs
    for i in range(number):
        dogs += [Dog()]
    for i in range(time):
        for hwo in dogs:
            hwo.move()
        for hwo in dogs:
            hwo.d_move()


def pole():
    sh = 10
    t.shapesize(0.01)
    t.speed(0)
    t.penup()
    t.width(sh)
    t.goto(0.5 * (a + size * d_size) + sh / 2, 0.5 * (b + size * d_size) + sh / 2)
    t.pendown()
    t.goto(0.5 * (a + size * d_size) + sh / 2, - 0.5 * (b + size * d_size) - sh / 2)
    t.goto(- 0.5 * (a + size * d_size) - sh / 2, - 0.5 * (b + size * d_size) - sh / 2)
    t.goto(- 0.5 * (a + size * d_size) - sh / 2, 0.5 * (b + size * d_size) + sh / 2)
    t.goto(0.5 * (a + size * d_size) + sh / 2, 0.5 * (b + size * d_size) + sh / 2)


d_size = 20
if input("ввести рекомендуемые настройки?(y/n): ") == "n":
    realism = (input("реализм (y/n): "))
    size = float(input("размер частицы (рек. 1): "))
    if realism == "y":
        push = int(input("сила отталкивания (рек. 400): "))
    number = int(input("количество (рек. 10): "))
    speed = int(input("скорость (рек. 4): "))
    time = int(input("время (рек. >1000): "))
    a, b = map(int, input("размеры баллона (рек. 600x400): ").split("x"))
    a -= size * d_size
    b -= size * d_size
    dogs = []
else:
    realism = (input("реализм (y/n): "))
    size = 1
    push = 400
    number = 10
    time = 10000
    speed = 4
    a = 600
    b = 400
    dogs = []
pole()
simulation()
