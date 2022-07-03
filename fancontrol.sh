#!/bin/bash

case "$1" in
    start)
        echo "Starting Fan"
        python3 /home/pi/.local/bin/fancontrol &
        ;;
    stop)
        echo "Stopping Fan"
        kill $(ps aux | grep -m 1 'python3 /home/pi/.local/bin/fancontrol' | awk '{ print $2 }')
        ;;
    *)
        echo "Usage: service fan start|stop"
        exit 1
        ;;
esac
exit 0
