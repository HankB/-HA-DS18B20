#!/usr/bin/env python3
'''
Script to control garage lighting according to the rules in the README
See http://oak:10080/HankB/home_automation-MQTT-sensors/src/branch/master/garage-door-position
An input liine woill look like (when the topic is included)
DEV/dorman/garage/door {"t": 1636341468, "position": "closed", "previous_position": "unknown", "selected": 52.738356590270996, "readings": [34.23209190368652, 59.18651819229126, 48.63312244415283, 52.738356590270996, 56.94172382354736]}

'''


import fileinput
import json
import time
import threading

timer_closed = 0  # timing light off, 0 => off. Otherwise time.time() to turn off
timer_open = 0    # timing light off, 0 => off. Otherwise time.time() to turn off
position = ""   # holds most recent position

# timer thread


def timer_thread():
    global timer_closed, timer_open, position
    print("timer thread started")
    while True:
        if timer_closed != 0 and timer_closed < time.time():     # timer expired?
            if position == "closed":    # still closed
                print("turn off light")
                os.system("/home/hbarta/bin/tplink-smartplug.py -t 192.168.20.62 -c off")
            timer_closed = 0            # reset timer
        if timer_open != 0 and timer_open < time.time():       # timer expired?
            print("turn off light")
            os.system("/home/hbarta/bin/tplink-smartplug.py -t 192.168.20.62 -c off")
            timer_open = 0              # reset timer
        time.sleep(10)                       # sleep 10 seconds


# main()
x = threading.Thread(target=timer_thread)
x.start()

for line in fileinput.input():
    (topic, payload) = line.split(' ', 1)
    jp = json.loads(payload)
    print('jp["position"]', jp["position"])
    position = jp["position"]
    if jp["position"] == 'closed':
        print("starting 3 min light off timer")
        timer_closed = time.time() + 180
    elif jp["position"] == 'open':
        print("turn on and start 10 min light off timer")
        os.system("/home/hbarta/bin/tplink-smartplug.py -t 192.168.20.62 -c on")
        timer_open = time.time() + 600
    else:
        print("unknown position received")
