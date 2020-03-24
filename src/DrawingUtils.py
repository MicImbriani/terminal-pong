import numpy as np


def cursor_reset_code():
    return "\033[2J\033[1;1H"


def cursor_visibilty_code(is_hidden):
    return "\033[?25" + ("h" if is_hidden else "l")


def colour_change_code(colour):
    return "\033[" + colour


def colour_reset_code():
    return "\033[0m"


def move_cursor_code(pos_xy, window_dims):
    for i in range(0, 2):
        if(pos_xy[i] < 0):
            pos_xy[i] = 0
        elif(pos_xy[i] > window_dims[i] - 1):
            pos_xy[i] = window_dims[i] - 1

    return "\033[" + str(pos_xy[1]) + ";" + str(pos_xy[0]) + "H"
