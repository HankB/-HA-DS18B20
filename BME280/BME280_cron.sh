#!/bin/sh

# command line arguments: description [host]
# topic example "home_automation/haut/dining_room/temp_humidity"
# sample crontab entry, every minute
# * * * * * /home/pi/bin/temp_humidity_cron.sh outside_temp_humidity mqtt >/tmp/temp_humidity_cron.txt 2>&1


if [ $# -eq 0 ]
then
    echo "Usage: $0 description [broker_host]"
    exit 1
fi

description=$1

shift

if [ $# -eq 0 ]
then
    host=localhost      #default
else
    host=$1
fi

# ID our host
HOSTNAME=`hostname`

# add user's !/bin to PATH
PATH=${HOME}/bin:$PATH

bme280-JSON.py 2>/tmp/temp_humidity_cron.txt | \
mosquitto_pub -s -t "HA/$HOSTNAME/$description/temp_humidity" -h $host
