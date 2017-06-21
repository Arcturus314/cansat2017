#!/bin/sh
# launcher.sh
# moves to correct directory and executes python script
# before running, confirm that the correct terminal (tty to check current terminal) and python script are used
# add to cron with:
#   1. sudo apt-get update
#   2. sudo apt-get install cron
#   3. sudo crontab -e
#   4. in ~/cansat2017/CanSat run chmod -x launcher.sh
#   4. add this line: @reboot sudo /bin/sh /home/chip/cansat2017/CanSat/launcher.sh >/dev/ttyGS0 2>&1

cd /
cd /home/chip/cansat2017/CanSat
python /home/chip/cansat2017/CanSat/control.py
cd /

