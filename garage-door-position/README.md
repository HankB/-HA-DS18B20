# Automate interior garage lighting

## Purpose

Determine if garage door is open or closed. This information will be used to automate interior garage lighting.

## Strategy

Measure distance to door from an HC-SR04 ultrasonic sensor mounted to a ceiling joist and connected to the Pi Zero used for outdoor temperature measurement. Infer garage door position and publish to MQTT. See [this investigation](http://prelude:8100/topics/HA/proximity-sensor/) for more detail on interpreting the readings. The short story is that if the reading is les than 40 cm, the door is open. This will be checked 1/second to provide quick response.

A Python script will take a single measurement which will then be piped to `mosquitto_pub` to publish. If feasible, a technique similar to the [MQTT_will](https://github.com/HankB/MQTT_will) project to avoid reconnecting to the broker 1/second.

An alternative is to poll the sensor and only publish changes in state. The concern with that is a missed MQTT message would result in inaction for the lighting. Initial effort will be to record 1/second readings in order to check for false open/closed inferences. The message will include all readings captured along with the one chosen to determine position.

## Usage

### Sender

On a Raspberry Pi in the garage. (`branddywine`)

NOTE: Path, host and topic appropriate for testing

```text
scp garage-door-position.py pi@brandywine:/home/pi/bin
# on dorman
/home/pi/bin/garage-door-position.py | mosquitto_pub -l -t "HA/${HOSTNAME}/garage/door" -h mqtt
# on any
mosquitto_sub -v -h mqtt -t DEV/\#
```

Once rolled out on `brandywine` the following entry in `/etc/rc.local` runs the process.

```text
runuser -u pi $(sleep 10; /home/pi/bin/garage-door-position.py | /usr/bin/mosquitto_pub -l -t "HA/${HOSTNAME}/garage/door" -h mqtt) 2>&1 >/tmp/rd.local.door.err &
```

That was an earlier version. `garage-door-position.py` has been modified to internally invoke the publish command. It seemed at one point that the previous code stopped publishing at some point. (Seems odd but that was during the shit show phase of rollout so could have been some other problem.) With the internal invocation of `mosquitto_pub` it will connect, publish one message, disconnect and exit. The following setup kicks it off.

```text
pi@brandywine:~ $ crontab -l
.
.
.
# m h  dom mon dow   command
*  * * * * /home/pi/bin/temp_humidity_cron.sh garage_north mqtt >/tmp/temp_humidity_cron.txt 2>&1

#@reboot sleep 10; /home/pi/bin/garage-door-position.py | /usr/bin/mosquitto_pub -l -t "HA/brandywine/garage/door" -h mqtt 2>&1 >/tmp/reboot.door.ttxtxt
@reboot /home/pi/bin/do-garage.sh
#@reboot sleep 10; /home/pi/bin/garage-door-position.py 2>&1 >/tmp/rd.local.door.err &

pi@brandywine:~ $ cat /home/pi/bin/do-garage.sh
#/bin/bash
sleep 20
/home/pi/bin/garage-door-position.py >/tmp/door.txt 2>&1

pi@brandywine:~ $ 
```

### Controller

On any convenient host. (`polana`. Eventually.)

NOTE: The python script that controls the TP-Link sockets is written in Python2 and not trivially portable to Python3. 

NOTE: Path and topic appropriate for production.

```text
scp control-garage-lighting.py hbarta@allred:/home/hbarta/bin
scp control-garage-lighting.py pi@polana:/home/pi/bin/
.
.
.
mosquitto_sub -v -h mqtt -t HA/+/garage/door | /home/hbarta/bin/control-garage-lighting.py
```

In `/etc/rc.local` the following works

```text
su hbarta -c 'sleep 10; /usr/bin/mosquitto_sub -v -h mqtt -t HA/+/garage/door | /home/hbarta/bin/control-garage-lighting.py 2>&1 > /tmp/rc.local.garage-light.err' &
```

Also can be put in user's cron.

```text
@reboot sleep 10; /usr/bin/mosquitto_sub -v -h mqtt -t HA/+/garage/door | /home/hbarta/bin/control-garage-lighting.py 2>&1 > /tmp/rc.local.garage-light.err
```

## Results

There are a *lot* of false open interpretations. Lights going on all times of day and night. Temperature was colder overnight. Is that the issue? From <> I get "Working Temperature:  -15°C to 70°C" which is 5°F on the low end. Didn't get that cold. Will try the shielding trick using a tube over the sensor/emitter. Inherent problem with the Raspberry Pi Zero?

First try - try another sensor. Also remount, perhaps better. Here are the readings

```text
/usr/bin/mosquitto_pub -h mqtt -t HA/brandywine/garage/door -m '{"position": "closed", "t": 1637340891, "readings": [256.2009572982788, 256.6957116127014, 257.0555329322815, 257.38264322280884, 257.0555329322815], "selected": 257.0555329322815, "previous_position": "unknown"}'


/usr/bin/mosquitto_pub -h mqtt -t HA/brandywine/garage/door -m '{"position": "open", "t": 1637341005, "readings": [35.103023052215576, 35.532355308532715, 36.11706495285034, 35.10711193084717, 35.622310638427734], "selected": 35.532355308532715, "previous_position": "closed"}'
```

The 'closed' distances are striking! And look correct. "Open" readings look better too. Will watch for a while.

## Errata

It will be necessary to schedule these by means other than `cron` since granularity of `cron` timing is 1/minute.

Alternatives [IR "avoidance" sensor](https://smile.amazon.com/gp/product/B07T91JXHW/)
