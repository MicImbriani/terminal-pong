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

    def getPos(self):
        return self._pos

    def getLastPos(self):
        return self._lastPos

    def setPos(self, pos):
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
        self._collidingWithWall = False

        # Collision with left and right walls
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

        paddleCollision = False

        # Collision with paddles
        p1Pos = paddles[0].getPos()
        p1HalfSize = paddles[0].getSize() / 2
        p2Pos = paddles[1].getPos()
        p2HalfSize = paddles[1].getSize() / 2
        collidingPaddle = paddles[0]

        # Left paddle
        if(self._pos[0] < p1Pos[0] and self._pos[1] <= p1Pos[1] + p1HalfSize and self._pos[1] >= p1Pos[1] - p1HalfSize):
            self._pos[0] = p1Pos[0]
            self._vel[0] *= -1
            paddleCollision = True
            collidingPaddle = paddles[0]

        # Right paddle
        elif(self._pos[0] > p2Pos[0] and self._pos[1] <= p2Pos[1] + p2HalfSize and self._pos[1] >= p2Pos[1]- p2HalfSize):
            self._pos[0] = p2Pos[0]
            self._vel[0] *= -1
            paddleCollision = True
            collidingPaddle = paddles[1]

        # Vertical velocity after paddle collision
        if(paddleCollision):
            if(BALL_SPIN):
                self._vel[1] += collidingPaddle.getVerticalVel() * PADDLE_STICKINESS

            if(BALL_RANDOM_SPEED):
                velNorm = self._calcNormVel()
                randomSpeed = random.uniform(self._maxSpeed * 0.5, self._maxSpeed * 0.8)
                self._vel = velNorm * randomSpeed

        # Collision with bottom and top walls
        if(self._pos[1] < 0):
            self._pos[1] = 0
            self._vel[1] *= -1
        elif(self._pos[1] > winDims[1] - 1):
            self._pos[1] = winDims[1] - 1
            self._vel[1] *= -1
