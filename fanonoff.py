#!/usr/bin/python
from signal import SIGINT, signal
import time
from gpiozero import LED

from . import logs


FAN_OFF_TEMP = 46.0
FAN_ON_TEMP = 52.0

fan = LED(21)


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
