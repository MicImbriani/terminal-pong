import numpy as np
import time
import math
from Constants import *
from Paddle import Paddle
from Controller import *
from timeit import default_timer as timer


class Player:


    def __init__(self, side, windowDims):
        self._score = 0
        self._side = side
        self._paddle = Paddle(side, windowDims)
        self._controller = Controller()
        self._isServing = False
        self._serveSpeed = windowDims[0] / 3 # "Should take roughly 3 seconds to cross the screen"


    def update(self, ball, windowHeight, dt):
        self._paddle.update(dt)

        # Position paddle based on controller input
        paddleSize = self._paddle.size
        newVertPos = (paddleSize / 2) + self._controller.dialPosition_0_1 * (windowHeight - paddleSize)
        self._paddle.setVerticalPos(newVertPos, windowHeight)

        # When serving, tie the ball's Y position to that of the paddle
        if(self._isServing):
            # Left faces into court with +X, right with -X
            xDir = -1 if self._side == Side.RIGHT else 1
            ball.pos = np.array([self._paddle.position[0] + (1 * xDir), self._paddle.position[1]])
            ball.velocity = np.array([0, 0])

            # Release ball
            if(self._controller.isButtonDown(Side.LEFT)):
                self._isServing = False
                ball.velocity = np.array([self._serveSpeed, self._paddle.verticalVelocity])

        # Paddle size boost
        if(self._controller.isButtonDown(Side.RIGHT)):
            self._paddle.activateDoubleSize()


    def incrementScore(self):
        self._score += 1


    def updateControllerState(self, dialPos_0_1, leftButtonDown, rightButtonDown):
        self._controller._dialPosition_0_1 = dialPos_0_1
        self._controller._buttonsDown[int(Side.LEFT)] = leftButtonDown
        self._controller._buttonsDown[int(Side.RIGHT)] = rightButtonDown
    

    def setAsServing(self):
        self._isServing = True


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
    def isServing(self):
        return self._isServing
