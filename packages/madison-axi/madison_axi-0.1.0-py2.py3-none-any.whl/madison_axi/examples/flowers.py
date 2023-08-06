import random
from madison_axi.axi import *


def draw_flower(x, y):
    pen_up()

    move_to(x, y)
    for _ in range(15):
        for _ in range(5):
            turn_left(random.randrange(-90, 90))
            move_forward(random.randrange(5, 10))
            pen_down()
            pen_up()
            move_to(x, y)
        y = y + 3

    for _ in range(5):
        turn_left(random.randrange(-90, 90))
        move_forward(random.randrange(1, 6))
        pen_down()
        pen_up()
        move_to(x, y)


def flower_scene():
    initialize()

    # stem 1
    move_to(-100, -145)
    point_in_direction(70)
    pen_down()
    for _ in range(25):
        move_forward(5)
        turn_left(1)
    for _ in range(20):
        move_forward(5)
        turn_right(1)

    x1 = get_x()
    y1 = get_y()
    pen_up()

    # stem 2
    move_to(-100, -145)
    point_in_direction(90)
    pen_down()
    for _ in range(25):
        move_forward(5)
        turn_left(1)

    x2 = get_x()
    y2 = get_y()
    pen_up()

    # stem 3
    move_to(-30, -145)
    point_in_direction(90)
    pen_down()
    for _ in range(15):
        move_forward(5)
        turn_left(1)

    x3 = get_x()
    y3 = get_y()

    # flowers
    draw_flower(x1, y1)
    draw_flower(x2, y2)
    draw_flower(x3, y3)

    cleanup()
    input("Done! Press Enter to close the program.")


if __name__ == "__main__":
    flower_scene()
