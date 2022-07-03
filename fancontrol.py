#!/usr/bin/python3

import os
import time
from os.path import exists

import RPi.GPIO as GPIO

# doc: https://gpiozero.readthedocs.io/

FAN_OFF_TEMP = 46.0
FAN_ON_TEMP = 52.0
FAN_MAX_TEMP = 58.0

SLEEP_INTERVAL = 10.0
GPIO_PIN = 12
MAX_LOG_SIZE_IN_BYTES = 1_000_000

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


def rotate_logs():
    pi_pathname = '/home/pi/.local/share/fancontrol'
    log_pathname = pi_pathname + '/logs'
    log_filename = log_pathname + '/log.txt'

    if not exists(pi_pathname):
        os.mkdir(pi_pathname)

    if not exists(log_pathname):
        os.mkdir(log_pathname)

    if not exists(log_filename):
        new_log_file = open(log_filename, 'w')
        new_log_file.close()

    filesize = os.path.getsize(log_filename)

    if filesize > MAX_LOG_SIZE_IN_BYTES:
        rotate_file = '{}/log-{}.txt'.format(pi_pathname, time.ctime())
        os.rename(log_filename, rotate_file)
        new_log_file = open(log_filename, 'w')
        new_log_file.close()


def log_temperature(temperature, message):
    log_filename = '/home/pi/.local/share/fancontrol/logs/log.txt'
    with open(log_filename, 'a') as f:
        logtext = '{} {} {}\n'.format(time.ctime(), temperature, message)
        f.write(logtext)


def main():
    duty_cycle = PWM_MAX_VALUE
    fan_is_on = False

    while True:
        rotate_logs()

        temperature = cpu_temp()

        if temperature > FAN_ON_TEMP and not fan_is_on:
            duty_cycle = PWM_NORMAL_VALUE
            pwm.ChangeDutyCycle(duty_cycle)
            fan_is_on = True
            log_temperature(temperature, 'fan on')

        elif temperature > FAN_MAX_TEMP:
            duty_cycle = PWM_MAX_VALUE
            pwm.ChangeDutyCycle(duty_cycle)
            fan_is_on = True
            log_temperature(temperature, 'thermal throttling is comming')

        elif fan_is_on and temperature < FAN_OFF_TEMP:
            duty_cycle = PWM_OFF_VALUE
            pwm.ChangeDutyCycle(duty_cycle)
            fan_is_on = False
            log_temperature(temperature, 'fan off')

        else:
            log_temperature(temperature, 'pwm status: {}'.format(duty_cycle))

        time.sleep(SLEEP_INTERVAL)


if __name__ == '__main__':
    main()
