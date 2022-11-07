#!/bin/sh
# meant to be run fron cron
# */5 * * * * /home/hbarta/bin/publish-freezer-temp.sh
/home/hbarta/bin/ds18b20-temp.py | sed -e "s/  //"|tr -d '\n'| /usr/bin/mosquitto_pub -s -t "HA/$(hostname)/kitchen/fridge_temp" -h mqtt
