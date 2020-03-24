import math
import time
from timeit import default_timer as timer
import numpy as np
from Constants import *
from Controller import Controller

if(PLATFORM_PI):
    from hardware.ControllerInterface import HardwareControllerInterface
else:
    from hardware.ControllerInterface import VirtualControllerInterface

from Ball import Ball
from Paddle import Paddle
from Display import Display
from hardware.LEDDisplay import LEDDisplay
from DrawingUtils import *
from Player import *


class Pong:


    MAX_SCORE = 30
    PHYSICS_SPEED = 1.0
    DISPLAY_WINNER_DURATION = 4.0


    def __init__(self):
        self._dt = 0.0
        self._time_s = 0.0
        self._gameWon = False
        self._gameWonTime_s = 0.0

        if(PLATFORM_PI):
            self._controllerInterface = HardwareControllerInterface()
        else:
            self._controllerInterface = VirtualControllerInterface()

        self._display = Display()
        dims = self._display.windowDims
        self._player1 = Player(Side.LEFT, dims)
        self._player2 = Player(Side.RIGHT, dims)
        self._ball = Ball(dims[0] / 2)

        self._serveCount = 0
        self._servingPlayer = self._player1
        self._winningPlayer = self._player1


    def run(self):
        self._initialise()
        running = True

        while(running):
            gameShouldEnd = self._gameWon and (self._time_s > self._gameWonTime_s + Pong.DISPLAY_WINNER_DURATION)

            if(gameShouldEnd):
                running = False

            frameStartTime = timer()

            self._handleInput()
            self._update(self._display.windowDims)
            self._draw()

            self._dt = (timer() - frameStartTime) * Pong.PHYSICS_SPEED

        self._shutdown()


    def _initialise(self):
        self._servingPlayer.setAsServing()


    def _handleInput(self):
        self._controllerInterface.update(self._dt)

        # Player 1 controller
        P1_dialRot_0_1 = self._controllerInterface.getDial1Pos()
        P1_LButtonDown = self._controllerInterface.isCon1But1Down()
        P1_RButtonDown = self._controllerInterface.isCon1But2Down()
        self._player1.updateControllerState(P1_dialRot_0_1, P1_LButtonDown, P1_RButtonDown)

        # Player 2 controller
        P2_dialRot_0_1 = self._controllerInterface.getDial2Pos()
        P2_LButtonDown = self._controllerInterface.isCon2But1Down()
        P2_RButtonDown = self._controllerInterface.isCon2But2Down()
        self._player2.updateControllerState(P2_dialRot_0_1, P2_LButtonDown, P2_RButtonDown)


    def _update(self, windowDims):
        self._time_s += self._dt

        # Update ball
        paddles = [self._player1.paddle, self._player2.paddle]
        self._ball.update(self._display.windowDims, paddles, self._dt)

        # Update players
        self._player1.update(self._ball, windowDims[1], self._dt)
        self._player2.update(self._ball, windowDims[1], self._dt)

        # Scoring
        if(self._ball.collidingWithSideWall):
            scoringPlayer = self._player1 if self._ball.wallCollisionSide == self._player2.side else self._player2
            scoringPlayer.incrementScore()
            self._serveCount += 1

            # Serving
            if(self._serveCount % 5 == 0):
                self._servingPlayer = self._player1 if self._servingPlayer == self._player2 else self._player2

            self._servingPlayer.setAsServing()

        # Check for winner
        if(not self._gameWon):
            self._checkWinCondition()

        # Debug data to host console
        if(PLATFORM_PI and not PRINT_TO_TERMINAL):
            self._printDebugInfo()


    def _checkWinCondition(self):
        self._gameWonTime_s = self._time_s

        if(self._player1.score >= Pong.MAX_SCORE):
            self._gameWon = True
            self._winningPlayer = self._player1
            return

        if(self._player2.score >= Pong.MAX_SCORE):
            self._gameWon = True
            self._winningPlayer = self._player2


    def _printDebugInfo(self):
        lines = [
            "Controller 1:",
            "   buttons:",
            "       left: -- %s",
            "       right: - %s",
            "   dial: ------ %f",
            "Left paddle:",
            "   pos: ------- %.2f",
            "   yVel: ------ %.2f",
            "   size: ------ %.2f",
            "   state: ----- %s",

            "Controller 2:",
            "   buttons:",
            "       left: -- %s",
            "       right: - %s",
            "   dial: ------ %f",
            "Right paddle:",
            "   pos: ------- %.2f",
            "   yVel: ------ %.2f",
            "   size: ------ %.2f",
            "   state: ----- %s",
            "Ball:",
            "   pos: ------ [%.2f, %.2f]",
            "   vel: ------ [%.2f, %.2f]"
        ]

        w = self._display.windowDims

        output = "\033[2J"

        for lineIdx in range(len(lines)):
            output += moveCursorCode([1, lineIdx + 1], w) + lines[lineIdx]

        ballVel = self._ball.getVel()
        paddles = [self._player1.paddle, self._player2.paddle]
        controllers = [self._player1.controller, self._player2.controller]

        print(output % (
            "DOWN" if controllers[0].isButtonDown(Side.LEFT) else "UP",
            "DOWN" if controllers[0].isButtonDown(Side.RIGHT) else "UP",
            controllers[0].getDialPosition_0_1(),
            paddles[0].getPos()[1],
            paddles[0].getVerticalVel(),
            paddles[0].getSize(),
            "DOUBLE" if paddles[0].isSizeBoostActive() else "NORMAL",
            "DOWN" if controllers[1].isButtonDown(Side.LEFT) else "UP",
            "DOWN" if controllers[1].isButtonDown(Side.RIGHT) else "UP",
            self._controllerInterface.getDial2GPIOReading(),
            paddles[1].getPos()[1],
            paddles[1].getVerticalVel(),
            paddles[1].getSize(),
            "DOUBLE" if paddles[1].isSizeBoostActive() else "NORMAL",
            self._ball.pos[0], self._ball.pos[1],
            ballVel[0], ballVel[1])
        )


    def _draw(self):
        # Terminal display
        self._display.begin()

        dimsX = self._display.windowDims[0]
        if(not self._gameWon):
            self._display.drawNet()
            self._display.drawScore(self._player2.score, [int(dimsX * 0.75), 4])
            self._display.drawScore(self._player1.score, [int(dimsX * 0.25), 4])
            self._display.drawPlayer(self._player1)
            self._display.drawPlayer(self._player2)
            self._display.drawBall(self._ball)
        else:
            self._display.drawWinScreen(self._winningPlayer)

        self._display.end()

        # LED displays
        if(PLATFORM_PI and LEDS_USED):
            self._LEDDisplay.setLEDs(float(self._ball.pos[0] / dimsX))


    def _shutdown(self):
        self._display.close()


def main():
    pong = Pong()
    pong.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pong.shutdown()
        print(colourResetCode())
        print(cursorVisibiltyCode())
