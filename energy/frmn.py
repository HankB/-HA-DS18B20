#!/usr/bin/env python

"""
Monitor TP-Link HS-100 smartplug to determine when freezer door is left ajar

Some of this code (validIP, encrypt, decrypt and contents of sendrecv) are
copied from tplink-smartplug.py (https://github.com/softScheck/tplink-smartplug)
and are covered by the following copyright.

# by Lubomir Stroetmann
# Copyright 2016 softScheck GmbH 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Now modified to format payload as JSON
"""

import socket
import argparse
import paho.mqtt.client as mqtt
import re
import time
import json

version = 0.4
verbose = 0

"""
Functions related to communicating with TP-Link socket
"""

# Check if IP is valid
def validIP(ip):
	try:
		socket.inet_pton(socket.AF_INET, ip)
	except socket.error:
		parser.error("Invalid IP Address.")
	return ip 

# see if we can resolve host
def validHost(h):
    try:
        addr = socket.gethostbyname(h)
    except:
        parser.error("could not resolve host "+ h)
    return addr
        

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
	key = 171
	result = "\0\0\0\0"
	for i in string: 
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171 
	result = ""
	for i in string: 
		a = key ^ ord(i)
		key = ord(i) 
		result += chr(a)
	return result

# Send command and receive reply 
def sendrecv(cmd):
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((addr, port))
        sock_tcp.send(encrypt(cmd))
        data = sock_tcp.recv(2048)
        sock_tcp.close()

        reply = decrypt(data[4:])
        return reply
    except socket.error:
        return None

"""
Functions related to publishing MQTT messages
"""

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if verbose: print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if verbose: print(msg.topic+" "+str(msg.payload))

def on_publish(client, userdata, mid):
    if verbose: print("on_publish(", client, userdata, mid, ")")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect("mqtt", 1883, 60)	# connect to my MQTT server

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface. (changed to non-blocking call)
client.loop_start()
### end of included code

def publish_power(timestamp, I, V, W): # I, V, P => amps, volts. watts
    #payload = "{0:12.0F}, {1:3.2F}, {2:3.1F}, {3:3.1F}" \
            #.format(timestamp,float(I), float(V), float(W))
    payload_json = json.dumps({ "t": timestamp, "current":I, "volts":V, "watts":W })
    if verbose: print("publishing", payload_json)
    client.publish(topic,payload_json, qos=0, retain=True)    

""" 
Delay to the next minute interval some integral number of intervals
from time zero.
"""
def delay_to_interval(minutes=15):
    delay_sec = minutes*60 - int(time.time())%(minutes*60)
    time.sleep(delay_sec)


"""
Application logic
"""

# Parse commandline arguments
parser = argparse.ArgumentParser(description="Freezer monitor v" + str(version))
host = parser.add_mutually_exclusive_group(required=True)
host.add_argument("-t", "--target", metavar="<ip>", 
                    help="Target IP Address", type=validIP)
host.add_argument("-n", "--name", metavar="<name>", 
                    help="Target host name", type=validHost)
parser.add_argument("-v", "--verbosity", 
                    help="increase output verbosity",
                    action="store_true")
parser.add_argument("-l", "--location", type=str,
                    help="subject [default \"basement_frzr\"]",
                    default="basement_frzr")
parser.add_argument("-i", "--interval", type=int,
                    help="interval, minutes [default 5]",
                    default=5)
args = parser.parse_args()
verbose = args.verbosity

topic = "HA/"+socket.gethostname()+"/"+args.location+"/power"


ip = args.target
port = 9999
if args.target is None:
    if verbose: print("Using ", args.name)
    addr = args.name
else:
    if verbose: print("Using ", args.target)
    addr = args.target
    
#args.interval = 5		# minutes
delay_to_interval(args.interval)

while True:    
    timestamp = int(time.time())
    reply = sendrecv('{"emeter":{"get_realtime":{}}}')
    # parse reply which looks like
    # {"emeter":{"get_realtime":{"current":1.743814,"voltage":123.531411,"power":112.291943,"total":15.761000,"
    if verbose: print(reply)
    fields=re.split('[:,]', reply) # isolate readings from the string
    if len(fields) != 12 or fields[0] != '{"emeter"':
        if verbose: print("Unexpected reply:\n   ", reply)
        current = voltage = power = 0
    else:
        current = fields[3]
        voltage = fields[5]
        power = fields[7]

    if verbose: print("c,v,p", current, voltage, power)
    publish_power(timestamp, current, voltage, power)
    delay_to_interval(args.interval)
