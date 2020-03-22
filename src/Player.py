import numpy as np
import time
import math
from Constants import *
from Paddle import Paddle
from Controller import *

from timeit import default_timer as timer

class Player:
    def __init__(self, side, windowDims):
        self._score = PLAYER_START_SCORE
        self._side = side
        self._paddle = Paddle(side, windowDims)
        self._controller = Controller()
        self._isServing = False
        self._serveSpeed = windowDims[0] / 3 # "Should take roughly 3 seconds to cross the screen"

    # Moves the paddle based on observations of the Controller's dial state
    def update(self, ball, windowHeight, dt):
        self._paddle.update(dt)

        # Position paddle based on controller input
        paddleSize = self._paddle.getSize()
        newVertPos = (paddleSize / 2) + self._controller.getDialPosition_0_1() * (windowHeight - paddleSize)
        self._paddle.setVerticalPos(newVertPos, windowHeight)

        # If serving, tie the ball's Y position to that of the paddle
        if(self._isServing):
            # Left faces into court with +X, right with -X
            facingDir = -1 if self._side == Side.RIGHT else 1
            ball.setPos(np.array([self._paddle.getPos()[0] + (1 * facingDir), self._paddle.getPos()[1]]))
            ball.setVel(np.array([0, 0]))

            # Release ball
            if(self._controller.isButtonDown(Buttons.LEFT)):
                self._isServing = False
                ball.setVel(np.array([self._serveSpeed, self._paddle.getVerticalVel()]))

        # Paddle size boost
        if(self._controller.isButtonDown(Buttons.RIGHT)):
            self._paddle.activateDoubleSize()

    def incrementScore(self):
        self._score += 1

    def updateControllerState(self, dialPos_0_1, leftButtonDown, rightButtonDown):
        self._controller.update(dialPos_0_1, leftButtonDown, rightButtonDown)
    
    def getController(self):
        return self._controller

    def getSide(self):
        return self._side

    def getPaddle(self):
        return self._paddle

    def getScore(self):
        return self._score

    def isServing(self):
        return self._isServing

    def setAsServing(self):
        self._isServing = True
