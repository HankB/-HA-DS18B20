#!/usr/bin/env bash
# Bash3 Boilerplate. Copyright (c) 2014, kvz.io

set -o errexit
set -o pipefail
set -o nounset
############### end of Boilerplate

# ad hoc script to publish garage position to
# MQTT server

while(:)
do
    /home/pi/testbin/garage-door-position.py
    sleep 5
done | mosquitto_pub -l -t "DEV/${HOSTNAME}/garage/door" -h mqtt