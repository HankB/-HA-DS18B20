#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import statistics
import json
import socket
import os

# --------------------------------------------------------------------
# PINS MAPPING AND SETUP
# --------------------------------------------------------------------

echoPIN = 24
triggerPIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(echoPIN, GPIO.IN)
GPIO.setup(triggerPIN, GPIO.OUT)

# --------------------------------------------------------------------
# MAIN FUNCTIONS
# --------------------------------------------------------------------


def distance():
    new_reading = False
    counter = 0
    distance = 0
    duration = 0

    # send trigger
    GPIO.output(triggerPIN, 0)
    time.sleep(0.000002)
    GPIO.output(triggerPIN, 1)
    time.sleep(0.000010)
    GPIO.output(triggerPIN, 0)
    time.sleep(0.000002)

    # wait for echo reading
    while GPIO.input(echoPIN) == 0:
        counter += 1
        if counter == 5000:
            new_reading = True
            break

    if new_reading:
        return False
    startT = time.time()

    # TODO check for pin never going high.
    while GPIO.input(echoPIN) == 1:
        pass
    feedbackT = time.time()

    # calculating distance
    if feedbackT == startT:
        distance = -1
    else:
        duration = feedbackT - startT
        soundSpeed = 34300  # cm/s
        distance = duration * soundSpeed / 2
    return distance

# --------------------------------------------------------------------
# MAIN LOOP
# --------------------------------------------------------------------

# Collect 5 readings and publish.


reading_count = 5
previous_position = "unknown"
topic = str.format("HA/{}/garage/door", socket.gethostname())


try:
    while True:
        timestamp=int(time.time());

        readings = []
        for i in range(reading_count):
            readings.append(distance())
            time.sleep(0.1)
        selected = statistics.median(readings)
        if selected < 40:
            position = "open"
        else:
            position = "closed"
        if position != previous_position:
            payload_json = json.dumps({ "t": timestamp, "position":position, 
                "previous_position":previous_position, "selected":selected, 
                "readings":readings })
            cmd = str.format("/usr/bin/mosquitto_pub -h mqtt -t {} -m \"{}\"",
                            topic, payload_json)
            print(cmd)
            os.system(cmd)            
            previous_position = position
        time.sleep(1)

finally:
    GPIO.cleanup()
