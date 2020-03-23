# Class representing a single hardware controller object with a rotating dial and 2 buttons
class Controller:


    class Button:
        LEFT = 0
        RIGHT = 1


    def __init__(self):
        self._dialPosition_0_1 = 0.5       # Position of the dial, between 0 and 1
        self._buttonsDown = [False, False] # State of the two buttons


    def isButtonDown(self, button):
        return self._buttonsDown[int(button)]


    def getDialPosition_0_1(self):
        return self._dialPosition_0_1


    def update(self, dialPos_0_1, leftButtonDown, rightButtonDown):
        self._dialPosition_0_1 = dialPos_0_1
        self._buttonsDown[int(Controller.Button.LEFT)] = leftButtonDown
        self._buttonsDown[int(Controller.Button.RIGHT)] = rightButtonDown
