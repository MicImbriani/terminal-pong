from Constants import PLATFORM_PI

if(PLATFORM_PI):
    import RPi.GPIO as GPIO
    import smbus


class Button:


    POLL_INTERVAL = 1.0 / 60.0


    def __init__(self):
        self._is_down = False
        self._state_change_timer = 0.0


    def _update_state_change_timer(self, delta):
        self._state_change_timer += delta


    @property
    def is_down(self):
        return self._is_down


    @is_down.setter
    def is_down(self, new_state):
        self._is_down = new_state


    @property
    def state_change_timer(self):
        return self._state_change_timer


class GPIOButton(Button):


    def __init__(self, GPIO_PIN):
        super().__init__()
        self._pin_number = GPIO_PIN
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)


    def update(self, dt_s):
        # Performs basic software debouncing by capping the rate at which of the button's state is updated
        self._update_state_change_timer(dt_s)

        if(self.state_change_timer > Button.POLL_INTERVAL):
            state = ButtonState.DOWN if GPIO.input(self._pin_number) == 1 else ButtonState.UP
            self._update_state_change_timer(-Button.POLL_INTERVAL)


class I2CButton(Button):


    def __init__(self, switch_value):
        super().__init__()
        self.I2C_ADDRESS = 0x20
        self.PORT_ON = 0xFF
        self._bus = smbus.SMBus(1)
        self._switch_value = switch_value


    def update(self, dt_s):
        self._update_state_change_timer(dt_s)

        if(self.state_change_timer > Button.POLL_INTERVAL):
            i2c_value = 0

            self._bus.write_byte(self.I2C_ADDRESS, self.PORT_ON)
            i2c_value = self._bus.read_byte(self.I2C_ADDRESS)

            # If the current pins reading is the same as the number registered for this button, then the button is down
            state = ButtonState.UP if i2c_value == self._switch_value else ButtonState.DOWN
            self._update_state_change_timer(-Button.POLL_INTERVAL)
