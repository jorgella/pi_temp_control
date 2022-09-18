#!/usr/bin/python
from signal import SIGINT, signal
import time
from gpiozero import LED

import os
from os.path import exists
from time import time


MAX_LOG_SIZE_IN_BYTES = 1_000_000
FAN_OFF_TEMP = 46.0
FAN_ON_TEMP = 52.0

fan = LED(21)


def rotate_logs():
    pi_pathname = os.path.curdir
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
    log_filename = f'{os.path.curdir}/logs/log.txt'

    with open(log_filename, 'a') as f:
        logtext = '{} {} {}\n'.format(time.ctime(), temperature, message)
        f.write(logtext)


def cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        return float(f.read())/1000


def main():
    # close fan at begining
    is_close = True
    fan.off()
    while True:
        logs.rotate_logs()

        temperature = cpu_temp()
        if is_close:
            if temperature >= FAN_ON_TEMP:
                logs.log_temperature(temperature, 'fan on')
                fan.on()
                is_close = False
        else:
            if temperature < FAN_OFF_TEMP:
                logs.log_temperature(temperature, 'fan off')
                fan.off()
                is_close = True

        time.sleep(2.0)


def handler(signal_received, frame):
    print('SIGINT or CTRL-C')
    exit(0)


if __name__ == '__main__':
    signal(SIGINT, handler)
    main()
