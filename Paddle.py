import numpy as np
from timeit import default_timer as timer
from Constants import Side

class Paddle:
    class SizeBoost:
        def __init__(self):
            self._active = False
            self._startTime = 0.0
            self._count = 0
            self._duration = 15.0
            self._maxActivations = 2

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
            self.setSize(self._defaultSize * 2)

            currentTime = timer()
            if(currentTime - self._sizeBoost._startTime > self._sizeBoost._duration):
                self._resetSize()
                self._sizeBoost._active = False
        else:
            self.setSize(self._defaultSize)

    def activateDoubleSize(self):
        if(not (self._sizeBoost._active) and self._sizeBoost._count < self._sizeBoost._maxActivations):
            self._sizeBoost._active = True
            self._sizeBoost._startTime = timer()
            self._sizeBoost._count += 1

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

    def getPos(self):
        return self._pos

    def getLastPos(self):
        return self._lastPos

    def getVerticalVel(self):
        return self._verticalVel

    def getSize(self):
        return self._size

    def getLastSize(self):
        return self._lastSize

    def isSizeBoostActive(self):
        return self._sizeBoost._active

    def setSize(self, size):
        self._lastSize = self._size
        self._size = size

    def _resetSize(self):
        self._lastSize = self._size
        self._size = self._defaultSize
