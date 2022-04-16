#!/usr/bin/env python3

'''
From bme-REPL.py found somewhere on the Interwebs
'''



import smbus2
import bme280
import time
import json

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)
timeStamp = int(time.time())

# the compensated_reading class has the following attributes
'''
print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)
'''

payload_json = json.dumps({ "t": timeStamp, "sensor":data.id, "temp":data.temperature,
    "humid":data.humidity, "press": data.pressure})
print(payload_json)
# there is a handy string representation too
# print(data)

