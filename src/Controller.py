from Constants import Side


# Class representing a single hardware controller object with a rotating dial and 2 buttons
class Controller:


    def __init__(self):
        self._dialPosition_0_1 = 0.5       # Position of the dial, between 0 and 1
        self._buttonsDown = [False, False] # State of the two buttons


    def isButtonDown(self, side):
        return self._buttonsDown[int(side)]


    @property
    def dialPosition_0_1(self):
        return self._dialPosition_0_1


    @property
    def buttonsDown(self):
        return self._buttonsDown
