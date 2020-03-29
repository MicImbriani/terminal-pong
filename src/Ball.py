import numpy as np
import math
import random
from Constants import *
from Paddle import Paddle


class Ball:


    SPIN_AFTER_COLLISION = True
    RANDOM_SPEED_AFTER_COLLISION = True
    MAX_SPEED = 60


    def __init__(self, dims_x):
        self._position = np.array([float(dims_x) / 2, 0.0], dtype=float)
        self._last_position = self._position
        self._velocity = np.array([0.0, 0.0], dtype=float)
        self._colliding_with_side_wall = False
        self._wall_collision_side = Side.LEFT


    def update(self, win_dims, paddles, dt):
        self._update_position(dt)
        self._handle_collision(paddles, win_dims)
        self._clamp_speed_below_maximum()


    def _update_position(self, dt):
        self._last_position = np.array(self._position)
        self._position[0] += self._velocity[0] * dt
        self._position[1] += (self._velocity[1] * dt) / 2


    def _handle_collision(self, paddles, win_dims):
        self._handle_wall_collision(win_dims)
        self._handle_paddle_collision(paddles)


    def _handle_wall_collision(self, win_dims):
        self._colliding_with_side_wall = False

        # Left
        if(self._position[0] < 0):
            self._position[0] = 0
            self._velocity = np.array([0.0, 0.0])
            self._wall_collision_side = Side.LEFT

            if(self._last_position[0] >= 0):
                self._colliding_with_side_wall = True

        # Right
        elif(self._position[0] > win_dims[0] - 1):
            self._position[0] = win_dims[0] - 1
            self._velocity = np.array([0.0, 0.0])
            self._wall_collision_side = Side.RIGHT

            if(self._last_position[0] <= win_dims[0] - 1):
                self._colliding_with_side_wall = True

        # Bottom
        if(self._position[1] < 0):
            self._position[1] = 0
            self._velocity[1] *= -1
        
        # Top
        elif(self._position[1] > win_dims[1] - 1):
            self._position[1] = win_dims[1] - 1
            self._velocity[1] *= -1


    def _handle_paddle_collision(self, paddles):
        # Get position and size information for the paddles
        p1_pos = paddles[0].position
        p1_half_size = paddles[0].size / 2
        p2_pos = paddles[1].position
        p2_half_size = paddles[1].size / 2

        # Determine whether the ball is colliding with the right or left paddles
        left_collision = self._position[0] < p1_pos[0] and self._position[1] <= p1_pos[1] + p1_half_size and self._position[1] >= p1_pos[1] - p1_half_size 
        right_collision = self._position[0] > p2_pos[0] and self._position[1] <= p2_pos[1] + p2_half_size and self._position[1] >= p2_pos[1]- p2_half_size

        # Update the state of the ball after a collision
        colliding_paddle = paddles[0]

        if(left_collision):
            self._position[0] = p1_pos[0]
            self._velocity[0] *= -1
        elif(right_collision):
            self._position[0] = p2_pos[0]
            self._velocity[0] *= -1
            colliding_paddle = paddles[1]

        # Adds some interesting spin effects to the ball after a collision
        if(left_collision or right_collision):
            self._update_vertical_vel_after_paddle_collision(colliding_paddle)


    def _update_vertical_vel_after_paddle_collision(self, colliding_paddle):
        # Inherit some of the paddle's vertical velocity allowing for 'chop' effects
        if(Ball.SPIN_AFTER_COLLISION):
            self._velocity[1] += colliding_paddle.vertical_velocity * Paddle.GRIP

        # Applys a random speed to the ball
        if(Ball.RANDOM_SPEED_AFTER_COLLISION):
            vel_norm = self._calc_norm_vel()
            random_speed = random.uniform(Ball.MAX_SPEED * 0.5, Ball.MAX_SPEED * 0.8)
            self._velocity = vel_norm * random_speed


    def _calc_norm_vel(self):
        speed = self._calc_speed()
        return self._velocity * 1.0 / speed


    def _calc_speed(self):
        speed = math.sqrt(math.pow(self._velocity[0], 2) + math.pow(self._velocity[1], 2))
        return speed


    def _clamp_speed_below_maximum(self):
        # Normalises velocity vector and scales to match maximum speed if MAX_BALL_SPEED is exceeded
        speed = self._calc_speed()
        if(speed > Ball.MAX_SPEED):
            self._velocity *= Ball.MAX_SPEED / speed


    @property
    def colliding_with_side_wall(self):
        return self._colliding_with_side_wall


    @property
    def wall_collision_side(self):
        return self._wall_collision_side


    @property
    def last_position(self):
        return self._last_position


    @property
    def position(self):
        return self._position


    @position.setter
    def position(self, pos):
        self._last_position = np.array(self._position)
        self._position = np.array(pos)


    @property
    def velocity(self):
        return self._velocity


    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity
