from timeit import default_timer as timer
import time
import math
from Constants import *
from hardware.GPIO_Map import *


if(PLATFORM_PI):
    import RPi.GPIO as GPIO
    import smbus

class ButtonState:
    UP = 0
    DOWN = 1

class ButtonCore:
    POLL_INTERVAL = 1.0 / 60.0

    def __init__(self):
        self._state = ButtonState.UP
        self._stateChangeTimer = 0.0

    def getState(self):
        return self._state

    def setState(self, newState):
        self._state = newState

    def updateStateChangeTimer(self, delta):
        self._stateChangeTimer += delta

    def getStateChangeTimer(self):
        return self._stateChangeTimer

class GPIOButton:
    def __init__(self, GPIO_PIN):
        self._core = ButtonCore()
        self._pinNumber = GPIO_PIN

        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def update(self, dt_s):
        # Performs software debouncing by capping the rate at which of the button's
        #state is updated
        self._core.updateStateChangeTimer(dt_s)

        if(self._core.getStateChangeTimer() > ButtonCore.POLL_INTERVAL):
            newState = ButtonState.DOWN if GPIO.input(self._pinNumber) == 1 else ButtonState.UP
            self._core.setState(newState)
            self._core.updateStateChangeTimer(-ButtonCore.POLL_INTERVAL)

    def getState(self):
        return self._core.getState()

class I2CButton:
    def __init__(self, switchValue):
        self.I2C_ADDRESS = 0x20
        self.PORT_ON = 0xFF
        self._bus = smbus.SMBus(1)
        self._core = ButtonCore()

        self._switchValue = switchValue

    def update(self, dt_s):
        self._core.updateStateChangeTimer(dt_s)

        if(self._core.getStateChangeTimer() > ButtonCore.POLL_INTERVAL):
            self._bus.write_byte(self.I2C_ADDRESS, self.PORT_ON)
            i2cvalue = self._bus.read_byte(self.I2C_ADDRESS)

            # If the current pins reading is the same as the number registered for this button, then
            # the button is down
            newState = ButtonState.UP if i2cvalue == self._switchValue else ButtonState.DOWN
            self._core.setState(newState)
            self._core.updateStateChangeTimer(-ButtonCore.POLL_INTERVAL)

    def getState(self):
        return self._core.getState()

class GPIODial:
    def __init__(self):
        self._reading_0_1 = 0.0
        self._stateHistory = [0, 0, 0, 0, 0]

        self._count = 0
        self._resetPin = 14
        self._testPin = 11

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._resetPin, GPIO.OUT)
        GPIO.output(self._resetPin, False)
        GPIO.setup(self._testPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def update(self):
        value = self.getInstantValue()
        self._shiftStateHistory()
        self._stateHistory[4] = value

    def _shiftStateHistory(self):
        for i in range(1, 5):
            self._stateHistory[i - 1] = self._stateHistory[i]

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

class ControllerInterface:
    def __init__(self):
        if(PLATFORM_PI):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)

            # Controller buttons using GPIO
            self._con1But1 = GPIOButton(GPIO_CON_1_BUT_1)
            self._con1But2 = GPIOButton(GPIO_CON_1_BUT_2)

            # Controller buttons using
            self._con2But1 = I2CButton(251)
            self._con2But2 = I2CButton(247)

            # Controller dial 1 data
            self.I2C_ADDRESS = 0x21
            self.CMD_CODE = 0b00100000
            self._bus = smbus.SMBus(1)

            # Controller dial 2
            self._gpioDial = GPIODial()

    def update(self, time_s):
        if(not PLATFORM_PI):
            return

        self._con1But1.update(time_s)
        self._con1But2.update(time_s)
        self._con2But1.update(time_s)
        self._con2But2.update(time_s)
        self._gpioDial.update()

    def isCon1But1Down(self):
        # TODO: Implement software debounce
        if(PLATFORM_PI):
            return self._con1But1.getState() == ButtonState.UP
        else:
            return True

    def isCon1But2Down(self):
        if(PLATFORM_PI):
            return self._con1But2.getState() == ButtonState.UP
        else:
            return True

    def isCon2But1Down(self):
        if(PLATFORM_PI):
            return self._con2But1.getState() == ButtonState.UP
        else:
            return True

    def isCon2But2Down(self):
        if(PLATFORM_PI):
            return self._con2But2.getState() == ButtonState.UP
        else:
            return True

    def getDial1Pos(self):
		# temp
        return 0.5		
		#
        self._bus.write_byte(self.I2C_ADDRESS, self.CMD_CODE)
        tmp = self._bus.read_word_data(self.I2C_ADDRESS, 0x00)
        stringBin = str(bin(tmp))

		# Making string same length
        binStr = stringBin[2:]
        output = ""
        if(len(binStr) < 16):
            output += "0" * (16 - len(binStr))

        output += binStr
        A = output[:4]
        B = output[4:8]
        C = output[8:12]
        D = output[12:16]

        result = D + A + B
        return 1.0 - float(int(result, 2) / 4092.0)

    def getDial2GPIOReading(self):
        return self._gpioDial.getInstantValue()

    def getDial2Pos(self):
        # temp
        return 0.5
        #
        
        return self._gpioDial.getInstantValue()
        # TODO: Get controller 2's dial value between 0 and 1
