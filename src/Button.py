from Constants import PLATFORM_PI


if(PLATFORM_PI):
    import RPi.GPIO as GPIO
    import smbus


class Button:


    POLL_INTERVAL = 1.0 / 60.0


    def __init__(self):
        self._isDown = False
        self._stateChangeTimer = 0.0


    def _updateStateChangeTimer(self, delta):
        self._stateChangeTimer += delta


    @property
    def isDown(self):
        return self._isDown


    @isDown.setter
    def isDown(self, newState):
        self._isDown = newState


    @property
    def stateChangeTimer(self):
        return self._stateChangeTimer


class GPIOButton(Button):


    def __init__(self, GPIO_PIN):
        super().__init__()
        self._pinNumber = GPIO_PIN
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)


    def update(self, dt_s):
        # Performs basic software debouncing by capping the rate at which of the button's state is updated
        self._updateStateChangeTimer(dt_s)

        if(self.stateChangeTimer > Button.POLL_INTERVAL):
            state = ButtonState.DOWN if GPIO.input(self._pinNumber) == 1 else ButtonState.UP
            self._updateStateChangeTimer(-Button.POLL_INTERVAL)


class I2CButton(Button):


    def __init__(self, switchValue):
        super().__init__()
        self.I2C_ADDRESS = 0x20
        self.PORT_ON = 0xFF
        self._bus = smbus.SMBus(1)
        self._switchValue = switchValue


    def update(self, dt_s):
        self._updateStateChangeTimer(dt_s)

        if(self.stateChangeTimer > Button.POLL_INTERVAL):
            i2cvalue = 0

            self._bus.write_byte(self.I2C_ADDRESS, self.PORT_ON)
            i2cvalue = self._bus.read_byte(self.I2C_ADDRESS)

            # If the current pins reading is the same as the number registered for this button, then the button is down
            state = ButtonState.UP if i2cvalue == self._switchValue else ButtonState.DOWN
            self._updateStateChangeTimer(-Button.POLL_INTERVAL)
