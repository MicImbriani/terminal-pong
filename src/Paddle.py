import numpy as np
from timeit import default_timer as timer
from Constants import Side


class Paddle:


    GRIP = 1.0


    class SizeBoost:
        DURATION = 15.0
        MAX_ACTIVATIONS = 2


        def __init__(self):
            self._active = False
            self._startTime = 0.0
            self._activationCount = 0


    def __init__(self, side, windowDims):
        self._defaultSize = 4.0
        self._size = self._defaultSize
        self._lastSize = self._defaultSize
        self._verticalVel = 0
        self._sizeBoost = Paddle.SizeBoost()

        paddleXPos = 3 if side == Side.LEFT else windowDims[0] - 3
        self._pos = np.array([paddleXPos, windowDims[1] / 2], dtype=float)
        self._lastPos = np.array(self._pos, dtype = float)


    def update(self, dt):
        self._verticalVel = (self._pos[1] - self._lastPos[1]) / dt

        # Disable the paddle size boost after 15 seconds
        if(self._sizeBoost._active):
            self.size = self._defaultSize * 2

            currentTime = timer()
            if(currentTime - self._sizeBoost._startTime > Paddle.SizeBoost.DURATION):
                self._resetSize()
                self._sizeBoost._active = False
        else:
            self.size = self._defaultSize


    def _resetSize(self):
        self._lastSize = self._size
        self._size = self._defaultSize


    def activateDoubleSize(self):
        if((not self._sizeBoost._active) and self._sizeBoost._activationCount < Paddle.SizeBoost.MAX_ACTIVATIONS):
            self._sizeBoost._active = True
            self._sizeBoost._startTime = timer()
            self._sizeBoost._activationCount += 1


    def setVerticalPos(self, verticalPos, winHeight):
        # Vertically clamp the paddle within the window
        newVerticalPos = verticalPos
        if(newVerticalPos - (self._size / 2) < 0):
            newVerticalPos = (self._size / 2)
        elif(newVerticalPos + (self._size / 2) > winHeight):
            newVerticalPos = winHeight - (self._size / 2)

        # Update position
        self._lastPos[1] = self._pos[1]
        self._pos[1] = newVerticalPos


    def isSizeBoostActive(self):
        return self._sizeBoost._active


    @property
    def position(self):
        return self._pos


    @property
    def lastPosition(self):
        return self._lastPosition


    @property
    def verticalVelocity(self):
        return self._verticalVel


    @property
    def size(self):
        return self._size


    @size.setter
    def size(self, size):
        self._lastSize = self._size
        self._size = size


    @property
    def lastSize(self):
        return self._lastSize
