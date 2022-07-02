#!/usr/bin/python3

import os
import time
from os.path import exists

from gpiozero import OutputDevice

# doc: https://gpiozero.readthedocs.io/

MIN_FAN_ON_TEMP = 48.0
MAX_FAN_OFF_TEMP = 56.0
SLEEP_INTERVAL = 5.0
GPIO_PIN = 17
MAX_LOG_SIZE_IN_BYTES = 1_000_000


def cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        return float(f.read()) / 1000


def rotate_logs():
    pi_pathname = '/home/pi/pi_temp_control'
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
    log_filename = '/home/pi/pi_temp_control/logs/log.txt'
    with open(log_filename, 'a') as f:
        logtext = '{} {} {}'.format(time.ctime(), temperature, message)
        f.write(logtext)


def main():
    fan = OutputDevice(GPIO_PIN)
    fan.off()

    while True:
        rotate_logs()

        temperature = cpu_temp()

        if temperature > MAX_FAN_OFF_TEMP and not fan.value:
            log_temperature(time.ctime(), temperature, 'fan on')
            fan.on()
        elif fan.value and temperature < MIN_FAN_ON_TEMP:
            log_temperature(time.ctime(), temperature, 'fan off')
            fan.off()
        else:
            log_temperature(temperature, 'ok')

        time.sleep(SLEEP_INTERVAL)


if __name__ == '__main__':
    main()
