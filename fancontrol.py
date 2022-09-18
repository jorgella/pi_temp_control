#!/usr/bin/python3

import time
from signal import SIGINT, signal
from sys import exit
from . import logs

import RPi.GPIO as GPIO

# doc: https://gpiozero.readthedocs.io/

FAN_OFF_TEMP = 46.0
FAN_ON_TEMP = 52.0
FAN_MAX_TEMP = 58.0

SLEEP_INTERVAL = 10.0
GPIO_PIN = 12


PWM_FREQUENCY = 200
PWM_MAX_VALUE = 100
PWM_NORMAL_VALUE = 60
PWM_OFF_VALUE = 0


GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PIN, GPIO.OUT)

pwm = GPIO.PWM(GPIO_PIN, PWM_FREQUENCY)
pwm.start(PWM_OFF_VALUE)


def cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        return float(f.read()) / 1000


def main():
    duty_cycle = PWM_MAX_VALUE
    fan_is_on = False

    while True:
        logs.rotate_logs()

        temperature = cpu_temp()

        if temperature > FAN_ON_TEMP and not fan_is_on:
            duty_cycle = PWM_NORMAL_VALUE
            pwm.ChangeDutyCycle(duty_cycle)
            fan_is_on = True
            logs.log_temperature(temperature, 'fan on')

        elif temperature > FAN_MAX_TEMP:
            duty_cycle = PWM_MAX_VALUE
            pwm.ChangeDutyCycle(duty_cycle)
            fan_is_on = True
            logs.log_temperature(temperature, 'thermal throttling is comming')

        elif fan_is_on and temperature < FAN_OFF_TEMP:
            duty_cycle = PWM_OFF_VALUE
            pwm.ChangeDutyCycle(duty_cycle)
            fan_is_on = False
            logs.log_temperature(temperature, 'fan off')

        else:
            logs.log_temperature(temperature, 'pwm status: {}'.format(duty_cycle))

        time.sleep(SLEEP_INTERVAL)


def handler(signal_received, frame):
    pwm.stop()
    GPIO.cleanup()

    print('SIGINT or CTRL-C')
    exit(0)


if __name__ == '__main__':
    signal(SIGINT, handler)
    main()
