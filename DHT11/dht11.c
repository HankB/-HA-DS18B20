#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define MAXTIMINGS 85
#define DHTPIN 7

/*
install wiringPi from https://github.com/WiringPi/WiringPi on Bullseye

gcc -Wall dht11.c -o dht11 -l wiringPi
*/

int dht11_dat[5] = {0, 0, 0, 0, 0};

typedef struct {
	float		temperature;		// degrees °F
	float		humidity;			// % relative humodity
	int			status;				// 0 => success, -1 = no good
}	DHT11_result;

DHT11_result read_dht11_dat(void)
{
	uint8_t laststate = HIGH;
	uint8_t counter = 0;
	uint8_t j = 0, i;
	DHT11_result	result;

	dht11_dat[0] = dht11_dat[1] = dht11_dat[2] = dht11_dat[3] = dht11_dat[4] = 0;

	pinMode(DHTPIN, OUTPUT);
	digitalWrite(DHTPIN, LOW);
	delay(18);
	digitalWrite(DHTPIN, HIGH);
	delayMicroseconds(40);
	pinMode(DHTPIN, INPUT);

	for (i = 0; i < MAXTIMINGS; i++)
	{
		counter = 0;
		while (digitalRead(DHTPIN) == laststate)
		{
			counter++;
			delayMicroseconds(1);
			if (counter == 255)
			{
				break;
			}
		}
		laststate = digitalRead(DHTPIN);

		if (counter == 255)
			break;

		if ((i >= 4) && (i % 2 == 0))
		{
			dht11_dat[j / 8] <<= 1;
			if (counter > 16)
				dht11_dat[j / 8] |= 1;
			j++;
		}
	}

	if ((j >= 40) &&
		(dht11_dat[4] == ((dht11_dat[0] + dht11_dat[1] + dht11_dat[2] + dht11_dat[3]) & 0xFF)))
	{
		result.temperature = dht11_dat[2] * 9. / 5. + 32;
		result.humidity = dht11_dat[0];
		result.status = 0;
	}
	else
	{
		result.temperature = result.humidity = 0.0;
		result.status = -1;
	}

	return result;
}

int main(void)
{
	if (wiringPiSetup() == -1)
		exit(1);

	DHT11_result r = read_dht11_dat();
	printf("T:%.2f, H:%.2f, S:%i\n", r.temperature, r.humidity, r.status);
	return (0);
}
