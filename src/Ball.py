import numpy as np
import math
import random
from Constants import *


class Ball:


    SPIN_AFTER_COLLISION = True
    RANDOM_SPEED_AFTER_COLLISION = True
    MAX_SPEED = 60


    def __init__(self, dimsX):
        self._position = np.array([float(dimsX) / 2, 0.0], dtype=float)
        self._lastPosition = self._position
        self._velocity = np.array([0.0, 0.0], dtype=float)
        self._collidingWithSideWall = False
        self._wallCollisionSide = Side.LEFT


    def update(self, winDims, paddles, dt):
        self._updatePosition(dt)
        self._handleCollision(paddles, winDims)
        self._clampSpeedBelowMaximum()


    def _updatePosition(self, dt):
        self._lastPos = np.array(self._position)
        self._position[0] += self._velocity[0] * dt
        self._position[1] += (self._velocity[1] * dt) / 2


    def _handleCollision(self, paddles, winDims):
        self._handleWallCollision(winDims)
        self._handlePaddleCollision(paddles)


    def _handleWallCollision(self, winDims):
        self._collidingWithWall = False

        # Left
        if(self._position[0] < 0):
            self._position[0] = 0
            self._velocity = np.array([0.0, 0.0])
            self._collisionSide = Side.LEFT

            if(self._lastPos[0] >= 0):
                self._collidingWithWall = True

        # Right
        elif(self._position[0] > winDims[0] - 1):
            self._position[0] = winDims[0] - 1
            self._velocity = np.array([0.0, 0.0])
            self._collisionSide = Side.RIGHT

            if(self._lastPos[0] <= winDims[0] - 1):
                self._collidingWithWall = True

        # Bottom
        if(self._position[1] < 0):
            self._position[1] = 0
            self._velocity[1] *= -1
        
        # Top
        elif(self._position[1] > winDims[1] - 1):
            self._position[1] = winDims[1] - 1
            self._velocity[1] *= -1


    def _handlePaddleCollision(self, paddles):
        # Get position and size information for the paddles
        p1Pos = paddles[0].position
        p1HalfSize = paddles[0].size / 2
        p2Pos = paddles[1].position
        p2HalfSize = paddles[1].size / 2

        # Determine whether the ball is colliding with the right or left paddles
        leftCollision = self._position[0] < p1Pos[0] and self._position[1] <= p1Pos[1] + p1HalfSize and self._position[1] >= p1Pos[1] - p1HalfSize 
        rightCollision = self._position[0] > p2Pos[0] and self._position[1] <= p2Pos[1] + p2HalfSize and self._position[1] >= p2Pos[1]- p2HalfSize

        # Update the state of the ball after a collision
        collidingPaddle = paddles[0]

        if(leftCollision):
            self._position[0] = p1Pos[0]
            self._velocity[0] *= -1
        elif(rightCollision):
            self._position[0] = p2Pos[0]
            self._velocity[0] *= -1
            collidingPaddle = paddles[1]

        # Adds some interesting spin effects to the ball after a collision
        if(leftCollision or rightCollision):
            self._updateVerticalVelAfterPaddleCollision()


    def _updateVerticalVelAfterPaddleCollision(self):
        # Inherit some of the paddle's vertical velocity allowing for 'chop' effects
        if(SPIN_AFTER_COLLISION):
            self._velocity[1] += collidingPaddle.getVerticalVel() * PADDLE_STICKINESS

        # Applys a random speed to the ball
        if(RANDOM_SPEED_AFTER_COLLISION):
            velNorm = self._calcNormVel()
            randomSpeed = random.uniform(Ball.MAX_SPEED * 0.5, Ball.MAX_SPEED * 0.8)
            self._velocity = velNorm * randomSpeed


    def _calcNormVel(self):
        speed = self._calcSpeed()
        return self._velocity * 1.0 / speed


    def _calcSpeed(self):
        speed = math.sqrt(math.pow(self._velocity[0], 2) + math.pow(self._velocity[1], 2))
        return speed


    def _clampSpeedBelowMaximum(self):
        # Normalises velocity vector and scales to match maximum speed if MAX_BALL_SPEED is exceeded
        speed = self._calcSpeed()
        if(speed > Ball.MAX_SPEED):
            self._velocity *= Ball.MAX_SPEED / speed


    @property
    def collidingWithSideWall(self):
        return self._collidingWithSideWall


    @property
    def wallCollisionSide(self):
        return int(self._wallCollisionSide)


    @property
    def lastPosition(self):
        return self._lastPosition


    @property
    def position(self):
        return self._position


    @position.setter
    def position(self, pos):
        self._lastPosition = np.array(self._position)
        self._position = np.array(pos)


    @property
    def velocity(self):
        return self._velocity


    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity
