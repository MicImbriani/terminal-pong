import numpy as np
import time
import math
from Constants import *
from Paddle import Paddle
from Controller import *
from timeit import default_timer as timer


class Player:


    def __init__(self, side, window_dims):
        self._score = 12345
        self._side = side
        self._paddle = Paddle(side, window_dims)
        self._controller = Controller()
        self._is_serving = False
        self._serve_speed = window_dims[0] / 0.5 # "Should take roughly 3 seconds to cross the screen"


    def update(self, ball, window_height, dt):
        self._paddle.update(dt)

        # Position paddle based on controller input
        new_vert_pos = (self._paddle.size / 2) + self._controller.dial_position_0_1 * (window_height - self._paddle.size)
        self._paddle.set_vertical_pos(new_vert_pos, window_height)

        # When serving, tie the ball's Y position to that of the paddle
        if(self._is_serving):
            # Left faces into court with +X, right with -X
            xDir = -1 if self._side == Side.RIGHT else 1
            ball.position = np.array([self._paddle.position[0] + (1 * xDir), self._paddle.position[1]])
            ball.velocity = np.array([0, 0])

            # Release ball
            if(self._controller.is_button_down(Side.LEFT)):
                self._is_serving = False
                ball.velocity = np.array([50, self._paddle.vertical_velocity])
                ball.velocity = np.array([self._serve_speed, self._paddle.vertical_velocity])

        # Paddle size boost
        if(self._controller.is_button_down(Side.RIGHT)):
            self._paddle.activate_double_size()


    def increment_score(self):
        self._score += 1


    def update_controller_state(self, dial_pos_0_1, left_button_down, right_button_down):
        self._controller._dial_position_0_1 = dial_pos_0_1
        self._controller._buttons_down[Side.LEFT] = left_button_down
        self._controller._buttons_down[Side.RIGHT] = right_button_down
    

    def set_as_serving(self):
        self._is_serving = True


    @property
    def side(self):
        return self._side


    @property
    def paddle(self):
        return self._paddle


    @property
    def score(self):
        return self._score


    @property
    def is_serving(self):
        return self._is_serving


    @property
    def controller(self):
        return self._controller
