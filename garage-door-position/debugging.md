# debugging

Rollout to prod has been a real shit show. Time to step back, start with a methodical process and keep notes. Testing will begin on `allred` and when things look solid, migrate to `polana`. The sender is now running on the prod target `brandywine` but has issues. Work on executing `mosquitto_sub` within the Python script has been stashed. This has been (sort of) completed with the sender on `brandywine` and is not right.

## 2021-11-13 test on `allred`

Testing on `allred shows

```text
hbarta@allred:~/Programming/home_automation-MQTT-sensors/garage-door-position $ mosquitto_sub -v -h mqtt -t HA/+/garage/door | ./control-garage-lighting.py
timer thread started
Traceback (most recent call last):
  File "./control-garage-lighting.py", line 46, in <module>
    jp = json.loads(payload)
  File "/usr/lib/python3.7/json/__init__.py", line 348, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python3.7/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib/python3.7/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
^CException ignored in: <module 'threading' from '/usr/lib/python3.7/threading.py'>
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 1281, in _shutdown
    t.join()
  File "/usr/lib/python3.7/threading.py", line 1032, in join
    self._wait_for_tstate_lock()
  File "/usr/lib/python3.7/threading.py", line 1048, in _wait_for_tstate_lock
    elif lock.acquire(block, timeout):
KeyboardInterrupt

hbarta@allred:~/Programming/home_automation-MQTT-sensors/garage-door-position $
```

Capture using `mosquitto_sub` on another host shows the message

```text
HA/brandywine/garage/door {previous_position: open, position: closed, t: 1636820947, selected: 45.37837505340576, readings: [41.96416139602661, 47.67632484436035, 45.05126476287842, 49.47543144226074, 45.37837505340576]}
```

Quoting has been lost on the sender `garage-door-position.py`.

## sender

Kill running process

```text
pi@brandywine:~ $ ps -ef|grep garage
pi         245   236  0 Nov12 ?        00:00:00 /bin/sh -c /home/pi/bin/do-garage.sh
pi         246   245  0 Nov12 ?        00:00:00 /bin/sh /home/pi/bin/do-garage.sh
pi         578   246  1 Nov12 ?        00:15:38 /usr/bin/python3 /home/pi/bin/garage-door-position.py
pi       11957  8087  0 10:56 pts/0    00:00:00 grep --color=auto garage
pi@brandywine:~ $ kill 245 246 578
pi@brandywine:~ $ ps -ef|grep garage
pi       12094  8087  0 10:56 pts/0    00:00:00 grep --color=auto garage
pi@brandywine:~ $ 
```

Take a stab at the `shlex.quote()`. (copying to `~/bin` on brandywine.) No joy, Maybe just single quotes for the payload.

```python
            cmd = str.format("/usr/bin/mosquitto_pub -h mqtt -t {} -m \'{}\'",
                            topic, payload_json)
```

Seems to work, from the sniffer

```text
HA/brandywine/garage/door {"position": "open", "previous_position": "unknown", "readings": [4.133856296539307, 35.84311008453369, 36.32559776306152, 35.397422313690186, 36.2887978553772], "t": 1636823061, "selected": 35.84311008453369}
```

and <https://jsonlint.com/> deems it valid JSON. Now try a reboot. Great Success!

## controller

On `allred`, nothing running at the moment.

In `hbarta` crontab

```text
#@reboot sleep 10; /usr/bin/mosquitto_sub -v -h mqtt -t HA/+/garage/door | /home/hbarta/bin/control-garage-lighting.py 2>&1 > /tmp/rc.local.garage-light.err
```

Commands look OK, try running from a terminal (without redirecting output.) During test, there seemed to be a spurious "open" detected. Capture of messages is

```text
HA/brandywine/garage_north/temp_humidity {"t": 1636826341, "temp": 39.4, "humid":119.0, "rawT":"4A:34:66", "rawH":"FF:FF:2D", "retries":0}
HA/brandywine/garage/door {"position": "open", "t": 1636826349, "readings": [47.659969329833984, 10.49206256866455, 46.87081575393677, 10.528862476348877, 10.598373413085938], "previous_position": "closed", "selected": 10.598373413085938}
HA/brandywine/garage/door {"position": "closed", "t": 1636826350, "readings": [46.11846208572388, 10.361218452453613, 45.4601526260376, 50.914716720581055, 46.543705463409424], "previous_position": "open", "selected": 46.11846208572388}
HA/brandywine/garage_north/temp_humidity {"t": 1636826402, "temp": 39.5, "humid":119.0, "rawT":"4A:54:DD", "rawH":"FF:FF:2D", "retries":0}
HA/brandywine/garage_north/temp_humidity {"t": 1636826461, "temp": 39.5, "humid":119.0, "rawT":"4A:5C:64", "rawH":"FF:FF:2D", "retries":0}
CM/brandywine/NA/state {"t":1636826494, "status": "STILL connected", "load15": 0.10 }
HA/brandywine/garage_north/temp_humidity {"t": 1636826521, "temp": 39.3, "humid":119.0, "rawT":"4A:30:A2", "rawH":"FF:FF:2D", "retries":0}
HA/brandywine/garage_north/temp_humidity {"t": 1636826581, "temp": 39.0, "humid":119.0, "rawT":"49:F0:C8", "rawH":"FF:FF:2D", "retries":0}
HA/brandywine/garage_north/temp_humidity {"t": 1636826641, "temp": 39.4, "humid":119.0, "rawT":"4A:40:5A", "rawH":"FF:FF:2D", "retries":0}
HA/brandywine/garage/door {"position": "open", "t": 1636826674, "readings": [35.48328876495361, 36.39101982116699, 35.41377782821655, 35.96168756484985, 35.87990999221802], "previous_position": "closed", "selected": 35.87990999221802}
HA/brandywine/garage_north/temp_humidity {"t": 1636826702, "temp": 39.4, "humid":119.0, "rawT":"4A:38:1B", "rawH":"FF:FF:2D", "retries":0}
```

And corresponding output

```text
hbarta@allred:~/bin $ /usr/bin/mosquitto_sub -v -h mqtt -t HA/+/garage/door | /home/hbarta/bin/control-garage-lighting.py
timer thread started
jp["position"] closed
starting 3 min light off timer
jp["position"] open
turn on and start 10 min light off timer
Sent:      {"system":{"set_relay_state":{"state":1}}}
Received:  {"system":{"set_relay_state":{"err_code":0}}}
jp["position"] closed
starting 3 min light off timer
turn off light
Sent:      {"system":{"set_relay_state":{"state":0}}}
Received:  {"system":{"set_relay_state":{"err_code":0}}}
jp["position"] open
turn on and start 10 min light off timer
Sent:      {"system":{"set_relay_state":{"state":1}}}
Received:  {"system":{"set_relay_state":{"err_code":0}}}

```

Stopping test to emable `crontab` entry (with 20s delay.)

* test - slightly closing the door: light off after 3 minutes.
* test - fully open door: light on, off in ten minutes
* text - fully closed: command to turn off after 3 minutes

Still getting spurious readings:

```text
HA/brandywine/garage/door {"position": "open", "t": 1636828792, "readings": [11.08086109161377, 47.504591941833496, 10.561573505401611, 52.01462507247925, 10.937750339508057], "previous_position": "closed", "selected": 11.08086109161377}
HA/brandywine/garage/door {"position": "closed", "t": 1636828794, "readings": [51.02102756500244, 49.37320947647095, 47.88076877593994, 10.136330127716064, 43.12949180603027], "previous_position": "open", "selected": 47.88076877593994}
HA/brandywine/garage/door {"position": "open", "t": 1636828797, "readings": [48.412322998046875, 6.4113616943359375, 10.357129573822021, 9.621131420135498, 49.28734302520752], "previous_position": "closed", "selected": 10.357129573822021}
HA/brandywine/garage/door {"position": "closed", "t": 1636828799, "readings": [49.35685396194458, 47.69676923751831, 48.207879066467285, 51.552581787109375, 48.17107915878296], "previous_position": "open", "selected": 48.207879066467285}
```

Will leave running for a while to see how this goes. Will take a look at the sensor to see if there is an obvious reason for spurious readings. Monitor with

```text
mosquitto_sub -v -t +/brandywine/# -h mqtt
```