from Constants import *
import time

if(PLATFORM_PI):
    import RPi.GPIO as GPIO
    import smbus


class LEDDisplay:


    I2C_ADDR = 0x38
    LED_ON = 0x0F
    LED_OFF = 0xFF


    def __init__(self):
        if(not PLATFORM_PI or not LEDS_USED):
            return

        self._leds = [5,6,12,13,16,19,20,26]
        self._board_leds =  [0xFF - 2**0, 0xFF - 2**1, 0xFF - 2**2, 0xFF - 2**3, 0xFF - 2**4, 0xFF - 2**5, 0xFF - 2**6, 0xFF - 2**7]
        self._bus = smbus.SMBus(1) # Enable I2C bus

        self._initialize()


    def set_leds(self, ball_pos):
        for i in range(8):
            # Maximum width is 1, so 1 divided by n of possible states (8) = 0.125
            if (ball_pos >= 0.125 * i and ball_pos < (0.125 * (i + 1))):
                GPIO.output(self._leds[i],True)

                self._bus.write_byte(LEDDisplay.I2C_ADDR, self._board_leds[i])
            else:
                GPIO.output(self._LEDs[i],False)


    def turn_off_all(self):
        # TODO
        for led_idx in self._leds:
            GPIO.output(self._leds[led_idx], False)


    def _initialize(self):
        # Initialization for board on PI
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for i in range(8):
            GPIO.setup(self._leds[i], GPIO.OUT)
