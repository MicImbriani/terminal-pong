from Constants import *
import time

if(PLATFORM_PI):
    import RPi.GPIO as GPIO
    import smbus

class LEDDisplay:
    def __init__(self):
        if(not PLATFORM_PI or not LEDS_USED):
            return

        self._LEDs = [5,6,12,13,16,19,20,26]
        self._boardLEDs =  [0xFF - 2**0, 0xFF - 2**1, 0xFF - 2**2, 0xFF - 2**3, 0xFF - 2**4, 0xFF - 2**5, 0xFF - 2**6, 0xFF - 2**7]
        self._bus = smbus.SMBus(1) # Enable I2C bus
        self._I2C_ADDR = 0x38      # I2C base address
        self._LED_ON = 0x0F
        self._LED_OFF = 0xFF

        self._initialize()

    def setLEDs(self, ballPos):
        for i in range(8):
            # Maximum width is 1, so 1 divided by n of possible states (8) = 0.125
            if (ballPos >= 0.125 * i and ballPos < (0.125 * (i + 1))):
                GPIO.output(self._LEDs[i],True)

                self._bus.write_byte(self._I2C_ADDR, self._boardLEDs[i])
            else:
                GPIO.output(self._LEDs[i],False)

    def turnOffAll(self):
        # TODO
        for ledIdx in self._LEDs:
            GPIO.output(self._LEDs[ledIdx], False)

    def _initialize(self):
        # Initialization for board on PI
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for i in range(8):
            GPIO.setup(self._LEDs[i], GPIO.OUT)
