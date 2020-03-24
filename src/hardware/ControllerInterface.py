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
        self.i2c_address = 0x21
        self.cmd_code = 0b00100000
        self._bus = smbus.SMBus(1)

        # GPIO controller buttons 
        self._con1_but1 = GPIOButton(GPIO_CON_1_BUT_1)
        self._con1_but2 = GPIOButton(GPIO_CON_1_BUT_2)

        # I2C controller buttons 
        self._con2_but1 = I2CButton(251)
        self._con2_but2 = I2CButton(247)

        # GPIO controller dial
        self._gpio_dial1 = GPIODial()


    def update(self, time_s):
        self._con1_but1.update(time_s)
        self._con1_but2.update(time_s)
        self._con2_but1.update(time_s)
        self._con2_but2.update(time_s)
        self._gpio_dial.update()


    def is_con1_but1_down(self):
        return self._con1_but1.is_down


    def is_con1_but2_down(self):
        return self._con1_but2.is_down


    def is_con2_but1_down(self):
        return self._con2_but1.is_down


    def is_con2_but2_down(self):
        return self._con2_but2.is_down


    def get_dial1_pos(self):
        self._bus.write_byte(self.i2c_address, self.cmd_code)
        tmp = self._bus.read_word_data(self.i2c_address, 0x00)
        string_bin = str(bin(tmp))

		# Making string same length
        bin_str = string_bin[2:]
        output = ""
        if(len(bin_str) < 16):
            output += "0" * (16 - len(bin_str))

        output += bin_str
        A = output[:4]
        B = output[4:8]
        C = output[8:12]
        D = output[12:16]

        result = D + A + B

        return 1.0 - float(int(result, 2) / 4092.0)


    def get_dial2_pos(self):
        return self._gpioDial.get_instant_value()


class VirtualControllerInterface():


    def __init__(self):
        self._time_s = 0.0


    def update(self, time_s):
        self._time_s += time_s


    def is_con1_but1_down(self):
        return False


    def is_con1_but2_down(self):
        return False


    def is_con2_but1_down(self):
        return False


    def is_con2_but2_down(self):
        return False


    def get_dial1_pos(self):
        return ((math.sin(self._time_s * 2.0 + 4.0) + 1.0) / 2)


    def get_dial2_pos(self):
        return ((math.sin(self._time_s * 2.0 + 4.0) + 1.0) / 2)
