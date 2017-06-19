#!/bin/sh
# launcher.sh
# moves to correct directory and executes python script
# before running, confirm that the correct terminal (tty to check curren terminal) and python script are used
# add to cron with @reboot.sh /home/chip/launcher.sh >/dev/ttyGS0 2>&1

cd /
cd home/chip
sudo python test.py
cd /

