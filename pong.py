import math
import time
from timeit import default_timer as timer
import numpy as np
from Constants import *
from Controller import Controller
from hardware.ControllerInterface import ControllerInterface
#from hardware.Buzzer import Buzzer
from Ball import Ball
from Paddle import Paddle
from Display import Display
from hardware.LEDDisplay import LEDDisplay
from DrawingUtils import *
from Player import *

class Pong:
    def __init__(self):
        self._timePointA = 0.0
        self._timePointB = 0.0
        self._dt = 0.0
        self._time_s = 0.0
        self._running = True
        self._gameWon = False
        self._gameWonTime_s = 0.0
        self._displayWinnerDuration = 4.0

        self._controllerInterface = ControllerInterface()
        self._display = Display()
        #self._buzzer = Buzzer()
        self._LEDDisplay = LEDDisplay()
        dims = self._display.getWindowDims()
        self._player1 = Player(Side.LEFT, dims)
        self._player2 = Player(Side.RIGHT, dims)
        self._ball = Ball(dims[0] / 2)

        self._serveCount = 0
        self._servingPlayer = self._player1
        self._winningPlayer = self._player1

    def _initialise(self):
        dimsX = self._display.getWindowDims()[0]
        self._servingPlayer.setAsServing()
        #self._buzzer.start()

        # Disable divide by 0 warning
        np.seterr(divide = 'ignore')

    def _setIO(self):
        # Get data from hardware and populate all fields in the player's controllers
        # TODO: Get correct data from controllers
        self._controllerInterface.update(self._dt)

        # -------------- Player 1 controller --------------
        P1_dialRot_0_1 = self._controllerInterface.getDial1Pos()
        P1_LButtonDown = self._controllerInterface.isCon1But1Down()
        P1_RButtonDown = self._controllerInterface.isCon1But2Down()
        self._player1.updateControllerState(P1_dialRot_0_1, P1_LButtonDown, P1_RButtonDown)

        # -------------- Player 2 controller --------------
        if(AUTO_CONTROL_RIGHT):
            P2_dialRot_0_1 = ((math.sin(self._time_s * 5.0 + 4.0) + 1.0) / 2)
        else:
            P2_dialRot_0_1 = self._controllerInterface.getDial2Pos()

        P2_LButtonDown = self._controllerInterface.isCon2But1Down()
        P2_RButtonDown = self._controllerInterface.isCon2But2Down()#True if ((math.sin(self._time_s * 1.2) + 1) / 2) > 0.8 else False
        self._player2.updateControllerState(P2_dialRot_0_1, P2_LButtonDown, P2_RButtonDown)

    def printDebugInfo(self):
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

        w = self._display.getWindowDims()

        output = "\033[2J"

        for lineIdx in range(len(lines)):
            output += moveCursorCode([1, lineIdx + 1], w) + lines[lineIdx]

        ballPos = self._ball.getPos()
        ballVel = self._ball.getVel()
        paddles = [self._player1.getPaddle(), self._player2.getPaddle()]
        controllers = [self._player1.getController(), self._player2.getController()]

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
            ballPos[0], ballPos[1],
            ballVel[0], ballVel[1])
        )

    def _update(self, windowDims):
        self._time_s += self._dt

        # Update ball
        paddles = [self._player1.getPaddle(), self._player2.getPaddle()]
        self._ball.update(self._display.getWindowDims(), paddles, self._dt)

        # Update players
        self._player1.update(self._ball, windowDims[1], self._dt)
        self._player2.update(self._ball, windowDims[1], self._dt)

        # Scoring
        if(self._ball.isCollidingWithWall()):
            scoringPlayer = self._player1 if self._ball.getCollisionSide() != self._player1.getSide() else self._player2
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
            self.printDebugInfo()

        # Sounds
        #self._buzzer.update(self._dt)

    def _checkWinCondition(self):
        self._gameWonTime_s = self._time_s

        if(self._player1.getScore() >= MAX_SCORE):
            self._gameWon = True
            self._winningPlayer = self._player1
            return

        if(self._player2.getScore() >= MAX_SCORE):
            self._gameWon = True
            self._winningPlayer = self._player2

    def _draw(self):
        # ------------ Terminal display ------------
        self._display.begin()

        dimsX = self._display.getWindowDims()[0]
        if(not self._gameWon):
            self._display.drawNet()
            self._display.drawScore(self._player2.getScore(), [int(dimsX * 0.75), 4])
            self._display.drawScore(self._player1.getScore(), [int(dimsX * 0.25), 4])
            self._display.drawPlayer(self._player1)
            self._display.drawPlayer(self._player2)
            self._display.drawBall(self._ball)
        else:
            self._display.drawWinScreen(self._winningPlayer)

        self._display.end()

        # ------------ LED Displays ------------
        if(PLATFORM_PI and LEDS_USED):
            self._LEDDisplay.setLEDs(float(self._ball.getPos()[0] / dimsX))

    def run(self):
        self._initialise()

        while(self._running):
            if(self._gameWon and ((self._time_s > self._gameWonTime_s + self._displayWinnerDuration))):
                self._running = False

            self._timePointA = timer()

            self._setIO()
            self._update(self._display.getWindowDims())
            self._draw()

            self._timePointB = timer()
            self._dt = (self._timePointB - self._timePointA) * SIM_SPEED

        self._shutdown()

    def shutdown(self):
        self._display.close()
        #self._buzzer.close()
        self.turnOffAll()

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
