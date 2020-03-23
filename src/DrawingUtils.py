import numpy as np


def cursorResetCode():
    return "\033[2J\033[1;1H"


def cursorVisibiltyCode(isHidden):
    return "\033[?25" + ("h" if isHidden else "l")


def colourChangeCode(colour):
    return "\033[" + colour


def colourResetCode():
    return "\033[0m"


def moveCursorCode(pos_xy, windowDims):
    for i in range(0, 2):
        if(pos_xy[i] < 0):
            pos_xy[i] = 0
        elif(pos_xy[i] > windowDims[i] - 1):
            pos_xy[i] = windowDims[i] - 1

    return "\033[" + str(pos_xy[1]) + ";" + str(pos_xy[0]) + "H"
