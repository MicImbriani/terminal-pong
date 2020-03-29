import numpy as np
import sys
import os
import subprocess
import math
from Screen import Screen
from Colours import COLOURS
from DrawingUtils import *
from res.DisplayElements import *
from Constants import *


if(PLATFORM_PI):
    from serial import Serial


class Display:


    FONT_CHAR_WIDTH = 3
    FONT_CHAR_HEIGHT = 5
    SERIAL_BAUD_RATE = 115200
    SERIAL_ADDR = "/dev/ttyAMA0"


    def __init__(self):
        if(PLATFORM_PI):
            self._serial_port = Serial(Display.SERIAL_ADDR, Display.SERIAL_BAUD_RATE)
            if (self._serial_port.is_open() == False):
                self._serial_port.open()

        rows, columns = subprocess.check_output(['stty', 'size']).split()
        self._window_dims = np.array([int(columns), int(rows)], dtype=int)

        # The distance (in characters) between the centre positions of 7 seg digits
        self._num_char_centre_dist = int(Display.FONT_CHAR_WIDTH / 2) * 2 + 2

        self._net_pos_x = int(self._window_dims[0] / 2)
        self._screen = Screen(self._window_dims)

        print(colour_reset_code())

        # Reset cursor position
        self.print_output("\033[2J")

        # Hide cursor code
        self.print_output(cursor_visibilty_code(False))


    def print_output(self, str):
        if(PLATFORM_PI and not PRINT_TO_TERMINAL):
            self._serial_port.write(bytes(str, 'ASCII'))
        else:
            print(str)


    def begin(self):
        self._screen.clear()


    def end(self):
        self.print_output(self._screen.get_output_string())
        self._screen.swap_buffers()


    def draw_background(self):
        self.draw_net()


    def draw_net(self):
        for i in range(1, self._window_dims[1]):
            if((i + 1) % 3 == 1 or (i + 2) % 3 == 1):
                self._screen.set_colour_idx_at(list(COLOURS.keys()).index("net"), [self._net_pos_x, i])


    def draw_score(self, score, pos_centre):
        digits = [int(c) for c in str(score)]
        num_digits = len(digits)

        pos_centre_x = pos_centre[0]
        first_digit_pos_x = pos_centre_x - ((num_digits - 1) * (Display.FONT_CHAR_WIDTH + 1) // 2)

        for i in range(0, num_digits):
            digit_pos_centre = np.array([first_digit_pos_x + i * self._num_char_centre_dist, pos_centre[1]])
            self._draw_7_seg_number(digits[i], digit_pos_centre)


    def draw_player(self, player):
        paddle = player.paddle
        pos = np.around(paddle.position).astype(int)
        size = int(paddle.size)

        # Draw paddle
        for i in range(- size // 2, size // 2):
            p = np.around(np.array(pos) + np.array([0, i])).astype(int)
            colour_name = "paddle" + ("Left" if player.side == Side.LEFT else "Right")
            colour_code = list(COLOURS.keys()).index(colour_name)
            self._screen.set_colour_idx_at(colour_code, p)


    def draw_ball(self, ball):
        pos = np.around(ball.position).astype(int)
        self._screen.set_colour_idx_at(list(COLOURS.keys()).index("ball"), pos)


    def draw_win_screen(self, player):
        start_pos_tl = np.array([(self._window_dims[0] - win_text_width) // 2, (self._window_dims[1] - win_text_height) // 2])
        counter = 0

        for i in range(0, len(win_text_rle)):
            if(i % 2 == 0):
                for j in range(0, win_text_rle[i]):
                    x = counter % win_text_width
                    y = (counter - x) // win_text_width
                    counter += 1
                    p = start_pos_tl + np.array([x + 1, y + 1])
                    self._screen.set_colour_idx_at(list(COLOURS.keys()).index("text"), p)
            else:
                counter += win_text_rle[i]

        self._draw_7_seg_number(int(player.side) + 1, self._window_dims // 2)


    def _draw_7_seg_number(self, num, pos_centre):
        if(num < 0 or num > 9):
            print("7-segment display can only display single-digit numbers (got " + str(num) + ")") 
            input()
            return

        # Each number should be drawn relative to the CENTRE of the 7 segment block
        pos_centre[0] -= Display.FONT_CHAR_WIDTH // 2 + 1
        pos_centre[1] -= Display.FONT_CHAR_HEIGHT // 2 + 1

        for y in range(0, 5):
            for x in range(0, 3):
                pos = np.array(pos_centre).astype(int) + np.array([x + 1, y + 1])
                if (digits[num][y * 3 + x] == 1):
                    self._screen.set_colour_idx_at(list(COLOURS.keys()).index("text"), pos)


    def close(self):
        if(PLATFORM_PI):
            self._serial_port.close()

        self.print_output(cursor_visibilty_code(True))
        self.print_output(colour_reset_code())
        self.print_output(cursor_reset_code())


    @property
    def window_dims(self):
        return self._window_dims


    @property
    def net_pos_x(self):
        return self._net_pos_x
