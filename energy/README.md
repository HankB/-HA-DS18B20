# Support energy monitoring

Abandoned - please see <http://oak:8080/HankB/HA-energy> where this continues.

This is used to monitor the energy used by the basement freezer using a TP-Link HS-110
smart outlet. Loosely related to this is a script that monitors temperature using a DS18B20 temperature sensor connected to a Raspberry Pi Zero
(`.../home_automation-MQTT-sensors/DS18B20`).

This is a major rework of this reporeter based on challenges involved with migrating to Python 3. Instead of coding a custom Python script to collect the data and publish, the current approach will be to collect the information using `tplink_smartplug.py` to report energy usage and then script something to extract that and publish using `mosquitto_pub`. The job will then be run from a user cron rather than starting once and perform its own timing.

## collection

```text
hbarta@olive:~/Programming/HA/home_automation-MQTT-sensors/energy$ tplink_smartplug.py -t 192.168.20.64 -c energy
Sent:      {"emeter":{"get_realtime":{}}}
Received:  {"emeter":{"get_realtime":{"current":0.011559,"voltage":124.065373,"power":0,"total":201.495000,"err_code":0}}}
hbarta@olive:~/Programming/HA/home_automation-MQTT-sensors/energy$
```

The following can extract desired fields (once the `jq` package is installed.) (total field used for demonstration because power is zero at the moment.)

```text
hbarta@olive:~$ tplink_smartplug.py -t 192.168.20.64 -c energy |tail -1|sed s/Received://|jq -r .emeter.get_realtime.total
201.495
hbarta@olive:~$
```

Next task is to format as valid JSON with a timestamp.

echo "{ \"t\": $(date +%s), \"watts\": 201.495 }"

For more see the playgropund `try.sh`

# Requirements

```text
apt install jq
```

## Usage

```text
cp frmn_json.sh ~/bin
scp frmn_json.sh oak:bin
```

Add a suitable crontab entry

*/5 * * * /home/hbarta/bin/frmn_json.sh| /usr/bin/mosquitto_pub -h olive -t ""HA/"$(hostname)"/basement_frzr/power" -l

kitchen

## Deprecated

Everything past this point is deprecated.

## Usage/Installation

```text
hbarta@olive05:/mnt/home/hbarta/Programming/home_automation-MQTT-sensors/energy$ ./frmn.py -h
usage: frmn.py [-h] (-t <ip> | -n <name>) [-v] [-l LOCATION] [-i INTERVAL]

Freezer monitor v0.3

optional arguments:
  -h, --help            show this help message and exit
  -t <ip>, --target <ip>
                        Target IP Address
  -n <name>, --name <name>
                        Target host name
  -v, --verbosity       increase output verbosity
  -l LOCATION, --location LOCATION
                        subject [default "basement"]
  -i INTERVAL, --interval INTERVAL
                        interval, minutes [default 5]
hbarta@olive05:/mnt/home/hbarta/Programming/home_automation-MQTT-sensors/energy$ 
```

### systemd

```text
mkdir /home/hbarta/freezer_pwr
sudo apt install python-paho-mqtt
sudo cp *.service /etc/systemd/system/
sudo systemctl start freezer_pwr
sudo systemctl enable freezer_pwr
sudo systemctl status freezer_pwr
sudo systemctl start fridge_pwr
sudo systemctl enable fridge_pwr
sudo systemctl status fridge_pwr
```
## Modules

### Requirements

Install paho-mqtt following instructions at https://www.eclipse.org/paho/clients/python/.

* paho-mqtt module as above.

    `pip install paho-mqtt`
or

    `sudo apt install python-paho-mqtt`

## Status

* Working - publishes to oak.

## TODO

* Update TODO list ;)
* Done - Make topic command line arguments.
* <s>Recover from dropped MQTT server connection.</s>
* Open/Close connection for each sample to send.
* Investigate switch to libmosquitto
