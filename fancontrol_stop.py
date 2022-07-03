#!/usr/bin/python3

import RPi.GPIO as GPIO

GPIO_PIN = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PIN, GPIO.OUT)

pwm = GPIO.PWM(GPIO_PIN, 200)
pwm.stop()
GPIO.cleanup()
