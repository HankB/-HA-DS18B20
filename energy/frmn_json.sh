#!/bin/bash

# produce JSON formatted output suitable for piping into mosquitto_pub.


# collect info from smart plug
input=$(tplink_smartplug.py -t 192.168.20.64 -c energy | \
      tail -1|sed s/Received://)

# extract the fields
fields=$(echo $input | \
  jq -r '.emeter.get_realtime.current, 
         .emeter.get_realtime.voltage, 
         .emeter.get_realtime.power ')

# Format and write output
json=$(echo $(date +%s) $fields  |\
 awk '{print "{\"t\":",  $1, ", \"current\":", $2, \
      ", \"power\":", $3,", \"watts\":", $4, "}" }')

echo $json | tr -d  '\n'