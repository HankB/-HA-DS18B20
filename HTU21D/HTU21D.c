#include <unistd.h>

#include "wiringPi.h"
#include "wiringPiI2C.h"

#include "HTU21D.h"

// Get temperature
result getTemperature(int fd)
{
	//unsigned char buf [4];
	result R;
	wiringPiI2CWrite(fd, HTU21D_TEMP);
	delay(100);
	read(fd, R.buf, 3);
	unsigned int temp = (R.buf[0] << 8 | R.buf[1]) & 0xFFFC;
	R.buf[3] = '\0'; 	// clear the last byte
	// Convert sensor reading into temperature.
	// See page 14 of the datasheet
	double tSensorTemp = temp / 65536.0;
	R.val = -46.85 + (175.72 * tSensorTemp);
	return R;
}

// Get humidity
result getHumidity(int fd)
{
	//unsigned char buf [4];
	result		R;
	wiringPiI2CWrite(fd, HTU21D_HUMID);
	delay(100);
	read(fd, R.buf, 3);
  	unsigned int humid = (R.buf [0] << 8 | R.buf [1]) & 0xFFFC;
	// Convert sensor reading into humidity.
	// See page 15 of the datasheet
	double tSensorHumid = humid / 65536.0;
	R.val = -6.0 + (125.0 * tSensorHumid);
	return R;
}
