#class representing a single hardware controller object
class Buttons:
    LEFT = 0
    RIGHT = 1

class Controller:
    def __init__(self):
        self._dialPosition_0_1 = 0.5       # Position of the variable resistor dial, between 0 and 1
        self._buttonsDown = [False, False] # State of the two buttons

    def isButtonDown(self, button):
        return self._buttonsDown[int(button)]

    def getDialPosition_0_1(self):
        return self._dialPosition_0_1

    def update(self, dialPos_0_1, leftButtonDown, rightButtonDown):
        self._dialPosition_0_1 = dialPos_0_1
        self._buttonsDown[int(Buttons.LEFT)] = leftButtonDown
        self._buttonsDown[int(Buttons.RIGHT)] = rightButtonDown
