from Constants import *
from Hardware.GPIO_Map import GPIO_BUZZER
import time
from Sounds import soundData

if(PLATFORM_PI):
	import RPi.GPIO as GPIO

class Buzzer:
    def __init__(self):
        if(PLATFORM_PI):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_BUZZER, GPIO.OUT)
            self._PWM = GPIO.PWM(GPIO_BUZZER, 100)

			self._playTimer_s = 0.0
			self._currentSameple = -1
			self._currentFreq = 0
			self._currentDuration = 0

	def start(self):
		if(PLATFORM_PI):
			self._PWM.start(0)
			self._PWM.ChangeDutyCycle(1)

	def update(self, dt_s):
		self._playTimer_s += dt_s

		if(self._playTimer_s > self._currentDuration):
			self._playTimer_s -= self._currentDuration
			self._currentSample += 1

		self._currentFreq = data[self._currentSample][0]
		self._currentDuration = data[self._currentSample][1]
		setFreq(self._currentFreq)

    def close(self):
        if(PLATFORM_PI):
            self._PWM.stop()
            GPIO.cleanup()

    def setFreq(self, freq):
		if(PLATFORM_PI):
			self._PWM.ChangeFrequency(freq)
