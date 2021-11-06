# Automate interior garage lighting

## Purpose

Determine if garage door is open or closed. This information will be used to automate interior garage lighting.

## Strategy

Measure distance to door from an HC-SR04 ultrasonic sensor mounted to a ceiling joist and connected to the Pi Zero used for outdoor temperature measurement. Infer garage door position and publish to MQTT. See [this investigation](http://prelude:8100/topics/HA/proximity-sensor/) for more detail on interpreting the readings. The short story is that if the reading is les than 40 cm, the door is open. This will be checked 1/second to provide quick response.

A Python script will take a single measurement which will then be piped to `mosquitto_pub` to publish. If feasible, a technique similar to the [MQTT_will](https://github.com/HankB/MQTT_will) project to avoid reconnecting to the broker 1/second.

An alternative is to poll the sensor and only publish changes in state. The concern with that is a missed MQTT message would result in inaction for the lighting. Initial effort will be to record 1/second readings in order to check for false open/closed inferences. The message will include all readings captured along with the one chosen to determine position.

## Usage

```text
scp garage-door-position.py pi@dorman://home/pi/testbin
## Errata

It will be wise to filter saving these messages to avoid flooding the MQTT message database with these messages. It will also be necessary to schedule these by means other than `cron` since granularity of `cron` timing is 1/minute.

Alternatives [IR "avoidance" sensor](https://smile.amazon.com/gp/product/B07T91JXHW/)
