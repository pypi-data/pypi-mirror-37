from madison_axi.axi import *


def spiky_circle():
    initialize()

    move_to(100, 0)
    point_in_direction(180)
    pen_down()

    for i in range(15):
        move_forward(200)
        turn_right(192)

    cleanup()
    input("Done! Press Enter to close the program.")


if __name__ == "__main__":
    spiky_circle()
