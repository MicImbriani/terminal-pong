import time
from Constants import PLATFORM_PI

if(PLATFORM_PI):
    import RPi.GPIO as GPIO
    import smbus


class GPIODial():


    def __init__(self):
        self._count = 0
        self._resetPin = 14
        self._testPin = 11

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._resetPin, GPIO.OUT)
        GPIO.output(self._resetPin, False)
        GPIO.setup(self._testPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def update(self):
        pass


    def getInstantValue(self):
        self.count = 0
        GPIO.output(self._resetPin, True)
        time.sleep(0.001)
        GPIO.output(self._resetPin, False)

        while GPIO.input(self._testPin) == 0 and self.count < 300:
            self.count +=1

        x = float(math.sqrt(math.sqrt(self.count))) * 10
        a = (x - 15.0) / 27.0

        return a
