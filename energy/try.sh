#!/bin/bash

# Playground for formatting the desired outpuit

input=$(tplink_smartplug.py -t 192.168.20.64 -c energy |tail -1|sed s/Received://)
echo 'input:' $input

# parse
echo parse: |tr  '\n' ' '
echo $input | \
  jq -r '.emeter.get_realtime.current, 
         .emeter.get_realtime.voltage, 
         .emeter.get_realtime.power '| \
  tr  '\n' ' '

# reformat as JSON with timestamp

fields=$(echo $input | \
  jq -r '.emeter.get_realtime.current, 
         .emeter.get_realtime.voltage, 
         .emeter.get_realtime.power '| \
  tr  '\n' ' ')

echo
echo 'fields:' $fields
echo $(date +%s) $fields  | awk '{print "{\"t\":",  $1, ", \"current\":", $2, ", \"power\":", $3,", \"watts\":", $4, "}" }'
