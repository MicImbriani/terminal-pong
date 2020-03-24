from timeit import default_timer as timer
import time
import math
from Constants import *
from hardware.GPIO_Map import *
from Button import *


class HardwareControllerInterface:


    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.I2C_ADDRESS = 0x21
        self.CMD_CODE = 0b00100000
        self._bus = smbus.SMBus(1)

        # GPIO controller buttons 
        self._con1But1 = GPIOButton(GPIO_CON_1_BUT_1)
        self._con1But2 = GPIOButton(GPIO_CON_1_BUT_2)

        # I2C controller buttons 
        self._con2But1 = I2CButton(251)
        self._con2But2 = I2CButton(247)

        # GPIO controller dial
        self._gpioDial1 = GPIODial()


    def update(self, time_s):
        self._con1But1.update(time_s)
        self._con1But2.update(time_s)
        self._con2But1.update(time_s)
        self._con2But2.update(time_s)
        self._gpioDial.update()


    def isCon1But1Down(self):
        return self._con1But1.isDown


    def isCon1But2Down(self):
        return self._con1But2.isDown


    def isCon2But1Down(self):
        return self._con2But1.isDown


    def isCon2But2Down(self):
        return self._con2But2.isDown


    def getDial1Pos(self):
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


    def getDial2Pos(self):
        return self._gpioDial.getInstantValue()


class VirtualControllerInterface():


    def __init__(self):
        self._time_s = 0.0


    def update(self, time_s):
        self._time_s += time_s


    def isCon1But1Down(self):
        return False


    def isCon1But2Down(self):
        return False


    def isCon2But1Down(self):
        return False


    def isCon2But2Down(self):
        return False


    def getDial1Pos(self):
        return ((math.sin(self._time_s * 2.0 + 4.0) + 1.0) / 2)


    def getDial2Pos(self):
        return ((math.sin(self._time_s * 2.0 + 4.0) + 1.0) / 2)
