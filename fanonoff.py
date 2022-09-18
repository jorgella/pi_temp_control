#!/usr/bin/python
import re
from signal import SIGINT, signal
import time

from sqlalchemy import false
from gpiozero import LED

import os
from os.path import exists


MAX_LOG_SIZE_IN_BYTES = 1_000_000
FAN_OFF_TEMP = 45.0
FAN_ON_TEMP = 50.0

fan = LED(18)


def rotate_logs():
    pi_pathname = '/opt/fancontrol'
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
    log_filename = '/opt/fancontrol/logs/log.txt'

    with open(log_filename, 'a') as f:
        logtext = '{} {} {}\n'.format(time.ctime(), temperature, message)
        f.write(logtext)


def cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        return float(f.read())/1000


class FanOnOff:
    def __init__(self):
        self.is_off = True

    def poweroff_fan(self):
        self.is_off = True
        fan.off()

    def poweron_fan(self):
        fan.on()
        self.is_off = False

    def get_state(self):
        return 'fan off' if self.is_off else 'fan on'


def main():
    control = FanOnOff()
    control.poweroff_fan()

    while True:
        rotate_logs()

        temperature = cpu_temp()
        if control.is_off:
            if temperature >= FAN_ON_TEMP:
                control.poweron_fan()
        elif temperature < FAN_OFF_TEMP:
            control.poweroff_fan()

        log_temperature(temperature, control.get_state())

        time.sleep(10.0)


if __name__ == '__main__':
    main()
