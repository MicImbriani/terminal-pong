import numpy as np
from timeit import default_timer as timer
from Constants import Side


class Paddle:


    GRIP = 1.0
    DEFAULT_SIZE = 4.0


    class SizeBoost:
        DURATION = 15.0
        MAX_ACTIVATIONS = 2


        def __init__(self):
            self._active = False
            self._start_time = 0.0
            self._activation_count = 0


    def __init__(self, side, window_dims):
        self._size = Paddle.DEFAULT_SIZE
        self._last_size = Paddle.DEFAULT_SIZE
        self._vertical_vel = 0
        self._size_boost = Paddle.SizeBoost()

        paddle_x_pos = 3 if side == Side.LEFT else window_dims[0] - 3
        self._pos = np.array([paddle_x_pos, window_dims[1] / 2], dtype=float)
        self._last_pos = np.array(self._pos, dtype = float)


    def update(self, dt):
        self._vertical_vel = (self._pos[1] - self._last_pos[1]) / dt

        # Disable the paddle size boost after 15 seconds
        if(self._size_boost._active):
            self.size = Paddle.DEFAULT_SIZE * 2

            current_time = timer()
            if(current_time - self._size_boost._start_time > Paddle.SizeBoost.DURATION):
                self._reset_size()
                self._size_boost._active = False
        else:
            self.size = Paddle.DEFAULT_SIZE


    def _reset_size(self):
        self._last_size = self._size
        self._size = Paddle.DEFAULT_SIZE


    def activate_double_size(self):
        if((not self._size_boost._active) and self._size_boost._activation_count < Paddle.SizeBoost.MAX_ACTIVATIONS):
            self._size_boost._active = True
            self._size_boost._start_time = timer()
            self._size_boost._activation_count += 1


    def setVerticalPos(self, vertical_pos, win_height):
        # Vertically clamp the paddle within the window
        new_vertical_pos = vertical_pos

        if(new_vertical_pos - (self._size / 2) < 0):
            new_vertical_pos = (self._size / 2)
        elif(new_vertical_pos + (self._size / 2) > win_height):
            new_vertical_pos = win_height - (self._size / 2)

        # Update position
        self._last_pos[1] = self._pos[1]
        self._pos[1] = new_vertical_pos


    def isSizeBoostActive(self):
        return self._vertical_vel._active


    @property
    def position(self):
        return self._pos


    @property
    def lastPosition(self):
        return self._last_position


    @property
    def verticalVelocity(self):
        return self._vertical_vel


    @property
    def size(self):
        return self._size


    @size.setter
    def size(self, size):
        self._last_size = self._size
        self._size = size


    @property
    def lastSize(self):
        return self._last_size
