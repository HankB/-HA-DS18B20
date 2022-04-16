# support BME280 sensor

## Motivation

The HTU21D can have trouble with the humidity reading going off scale and occasionally produces spurious readings. 

The BME280 module in hand has both SPI and I2C pins and the SPI interface 

And seems not to be working. :( Soldered pins on another and it does seem to work, but does not provide humidity.

Found  a C program that reads the DHT11 and wish to use C for the BME 280 as well. Found one at https://github.com/andreiva/raspberry-pi-bme280. Even puts out the results formatted as JSON! But it requires WiringPi lib.

I should have made a note of the source for the 2 Python scripts as I can't find one of them now. Did find samples at https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python/ along with Python code for the DHT11. I have a tab open to one of the pages: <https://pypi.org/project/RPi.bme280/>

And requirements.

## Deploy

```
sudo apt install python3-smbus
sudo raspi-config   # enable I2C
sudo apt install mosquitto-clients
```

Typical output

```text
hbarta@sodusx:~/Programming/BME280 $ ./bmp280.py
Temperature in Celsius : 19.97 C
Temperature in Fahrenheit : 67.95 F
Pressure : 986.84 hPa 
hbarta@sodusx:~/Programming/BME280 $ 
```

crontab entry

```text
* * * * * /home/hbarta/bin/BME280_cron.sh master_bedroom mqtt >/tmp/temp_humidity_cron.txt 2>&1
```
