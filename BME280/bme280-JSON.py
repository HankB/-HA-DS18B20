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
# there is a handy string representation too
# print(data)

output w/ sensor ID
payload_json = json.dumps({ "t": timeStamp, "sensor":str(data.id), "temp":data.temperature,
    "humid":data.humidity, "press": data.pressure})
{"t": 1650071788, "sensor": "ab2231e9-f8a8-4401-bb3b-5e64b9bdd82a", "temp": 20.66131623799447, "humid": 40.14417116321544, "press": 986.8545360477743}

With rounding
{"t": 1650072149, "temp": 21.23, "humid": 38, "press": 987.05}
'''

payload_json = json.dumps({ "t": timeStamp, "temp":round(data.temperature/5*9+32, 2), 
    "humid":round(data.humidity), "press":round(data.pressure, 2)})
print(payload_json, end = '')
