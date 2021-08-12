# fetch weather conditions

Publish to an MQTT broker. These scripts will exercise a different model
than other efforts. The code that produces the readings will write them to
stdout and the program `mosquitto_pub` will be used to publish to the MQTT
broker.
Several weather providers were tried with following results.
* OpenWeatherMap - Initial tests indicate infrequent updates
* Accuweather - Free tier allows 50 calls/day. Every half hour
* Dark Sky - allowa up ro 1000 calls/day on free tier. Seems to have
frequent updates.
* 

## Requirements

* API keys from the various providers
* Mosquitto client programs

    `apt install -y mosquitto-clients`

## testing

```text
./darksky.py -k 86d2e20ab0f3a752ca6e96f14a9db4e1 -l 41.866611,-88.160051 -t
```

```text
hbarta@olive:~/Programming/HA/home_automation-MQTT-sensors/weather$ ./darksky.py -k 86d2e20ab0f3a752ca6e96f14a9db4e1 -l 41.866611,-88.160051 -t
{"t": 1628738803, "msg": {"latitude": 41.866611, "longitude": -88.160051, "timezone": "America/Chicago", "currently": {"time": 1513630000, "summary": "Partly Cloudy", "icon": "partly-cloudy-day", "nearestStormDistance": 19, "nearestStormBearing": 215, "precipIntensity": 0, "precipProbability": 0, "temperature": 44.28, "apparentTemperature": 40.6, "dewPoint": 36.68, "humidity": 0.74, "pressure": 1012.25, "windSpeed": 6.44, "windGust": 13.92, "windBearing": 241, "cloudCover": 0.37, "uvIndex": 1, "visibility": 8.19, "ozone": 324.26}, "offset": -6}}hbarta@olive:~/Programming/HA/home_automation-MQTT-sensors/weather$ 
```

## Status

OpenWeatherClient variant set aside for the moment. It seems to update too infrequently.
