#!/bin/sh
# launcher.sh
# moves to correct directory and executes python script
# before running, confirm that the correct terminal (tty to check current terminal) and python script are used
# add to cron with:
#   0. in /etc/login.defs change LOGIN_TIMEOUT value to 0
#   1. sudo apt-get update
#   2. sudo apt-get install cron
#   3. sudo crontab -e
#   4. add this line: @reboot  sleep 10 && /usr/bin/python /home/chip/cansat2017/CanSat/control.py >/dev/ttyGS0 2>&1
#   5. add this line: @reboot stty /dev/ttyS0 9600 to change XBEE serial port to 9600 baud

cd /
cd /home/chip/cansat2017/CanSat
python /home/chip/cansat2017/CanSat/control.py
cd /

