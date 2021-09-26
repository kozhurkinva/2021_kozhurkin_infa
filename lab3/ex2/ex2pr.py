import turtle as t


def print_t(number):
    with open("ex2txt.txt") as txt:
        number_t = list(map(int, txt.read().split("\n")[number].split()))
    k = 0
    for j in range(len(number_t)):
        t.right(45 * number_t[j] * ((j + 1) % 2))
        t.forward(50 * number_t[j] * (j % 2) * (1 + k * (2 ** .5 - 1)))
        k = (k + ((j + 1) % 2) * (number_t[j] % 2)) % 2


numbers = list(map(int, list(input())))
t.speed(0)
t.shape("turtle")
t.penup()
t.goto(-50 * len(numbers), 50)
for i in numbers:
    t.pendown()
    print_t(i)
    t.penup()
    t.forward(100)
