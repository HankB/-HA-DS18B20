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

and <https://jsonlint.com/> deems it valid JSON.