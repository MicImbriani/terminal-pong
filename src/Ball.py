import numpy as np
import math
import random
from Constants import *

class Ball:
    def __init__(self, dimsX):
        self._pos = np.array([float(dimsX) / 2, 0.0], dtype=float)
        self._lastPos = np.array(self._pos) # for erasing the previous ball position
        self._vel = np.array([0.0, 0.0], dtype=float)
        self._collidingWithWall = False
        self._collisionSide = Side.LEFT
        self._maxSpeed = 60

    def update(self, winDims, paddles, dt):
        self._lastPos = np.array(self._pos)
        self._pos[0] += self._vel[0] * dt
        self._pos[1] += (self._vel[1] * dt) / 2

        self._handleCollision(paddles, winDims)
        self._clampSpeed()

    def isCollidingWithWall(self):
        return self._collidingWithWall

    def getCollisionSide(self):
        return int(self._collisionSide)

    def getLastPos(self):
        return self._lastPos

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._lastPos = np.array(self._pos)
        self._pos = np.array(pos)

    def setVel(self, vel):
        self._vel = vel

    def getVel(self):
        return self._vel

    def _calcSpeed(self):
        speed = math.sqrt(math.pow(self._vel[0], 2) + math.pow(self._vel[1], 2))
        return speed

    def _calcNormVel(self):
        speed = self._calcSpeed()
        return self._vel * 1.0 / speed

    def _clampSpeed(self):
        # Normalises velocity vector and scales to match maximum speed if MAX_BALL_SPEED is exceeded
        speed = self._calcSpeed()
        if(speed > self._maxSpeed):
            self._vel *= self._maxSpeed / speed


    def _handleCollision(self, paddles, winDims):
        self._handleWallCollision(winDims)
        self._handlePaddleCollision(paddles)


    def _handleWallCollision(self, winDims):
        self._collidingWithWall = False

        # Left and right walls
        if(self._pos[0] < 0):
            self._pos[0] = 0
            self._vel = np.array([0.0, 0.0])
            self._collisionSide = Side.LEFT

            if(self._lastPos[0] >= 0):
                self._collidingWithWall = True

        elif(self._pos[0] > winDims[0] - 1):
            self._pos[0] = winDims[0] - 1
            self._vel = np.array([0.0, 0.0])
            self._collisionSide = Side.RIGHT

            if(self._lastPos[0] <= winDims[0] - 1):
                self._collidingWithWall = True

        # Bottom and top walls
        if(self._pos[1] < 0):
            self._pos[1] = 0
            self._vel[1] *= -1

        elif(self._pos[1] > winDims[1] - 1):
            self._pos[1] = winDims[1] - 1
            self._vel[1] *= -1


    def _handlePaddleCollision(self, paddles):
        # Get position and size information for the paddles
        p1Pos = paddles[0].getPos()
        p1HalfSize = paddles[0].getSize() / 2
        p2Pos = paddles[1].getPos()
        p2HalfSize = paddles[1].getSize() / 2

        # Determine whether the ball is colliding with the right or left paddles
        leftCollision = self._pos[0] < p1Pos[0] and self._pos[1] <= p1Pos[1] + p1HalfSize and self._pos[1] >= p1Pos[1] - p1HalfSize 
        rightCollision = self._pos[0] > p2Pos[0] and self._pos[1] <= p2Pos[1] + p2HalfSize and self._pos[1] >= p2Pos[1]- p2HalfSize

        # Update the state of the ball after a collision
        collidingPaddle = paddles[0]

        if(leftCollision):
            self._pos[0] = p1Pos[0]
            self._vel[0] *= -1
        elif(rightCollision):
            self._pos[0] = p2Pos[0]
            self._vel[0] *= -1
            collidingPaddle = paddles[1]

        # Adds some interesting spin effects to the ball after a collision
        if(leftCollision or rightCollision):
            self._updateVerticalVelAfterPaddleCollision()


    def _updateVerticalVelAfterPaddleCollision(self):
        # Inherit some of the paddle's vertical velocity allowing for 'chop' effects
        if(BALL_SPIN):
            self._vel[1] += collidingPaddle.getVerticalVel() * PADDLE_STICKINESS

        # Applys a random speed to the ball
        if(BALL_RANDOM_SPEED):
            velNorm = self._calcNormVel()
            randomSpeed = random.uniform(self._maxSpeed * 0.5, self._maxSpeed * 0.8)
            self._vel = velNorm * randomSpeed

