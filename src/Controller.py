from Constants import Side


# Class representing a single hardware controller object with a rotating dial and 2 buttons
class Controller:


    def __init__(self):
        self._dial_position_0_1 = 0.5       # Position of the dial, between 0 and 1
        self._buttons_down = [False, False] # State of the two buttons


    def is_button_down(self, side):
        return self._buttons_down[int(side)]


    @property
    def dial_position_0_1(self):
        return self._dial_position_0_1


    @property
    def buttons_down(self):
        return self._buttons_down
