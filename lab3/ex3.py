import turtle as t
import random as rnd


def pole():
    t.goto(-1000, 0)
    t.goto(1000, 0)
    t.penup()
    t.goto(400, 0)
    t.pendown()


def move(x, y, y_speed):
    t.goto(x, y)
    if y <= 0 and y_speed <= 0:
        return [x + x_speed, y + y_speed, - 0.5 * y_speed + d_y_speed]
    else:
        return [x + x_speed, y + y_speed, y_speed - d_y_speed]


x_speed = -2 - 1 * rnd.random()
y_speed = 10 + 10 * rnd.random()
d_y_speed = 0.1 + 0.5 * rnd.random()
t.speed(0)
t.shape("turtle")
t.left(180)
pole()
x = 400
y = 0
for i in range(99999999999999):
    x, y, y_speed = move(x, y, y_speed)