#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>

#include "wiringPi.h"
#include "wiringPiI2C.h"

#include "HTU21D.h"

// format as "nn:nn:nn" where "nn" is hexadecimal 
// provide the output buffer
const char* formatBuf(unsigned char buf[4], char outbuf[10])
{
	snprintf( outbuf, 10, "%02X:%02X:%02X", buf[0], buf[1], buf[2]);
	return outbuf;
}

int main ()
{
	int fd = wiringPiI2CSetup(HTU21D_I2C_ADDR);
	if ( 0 > fd )
	{
		fprintf (stderr, "Unable to open I2C device: %s\n", strerror (errno));
		exit (-1);
	}
	result temperature = getTemperature(fd);
	char	temp_out_buf[10];
	result humidity = getHumidity(fd);
	char	humid_out_buf[10];
	
	    printf("{\"t\": %ld, \"temp\":%5.1f, \"humid\":%5.1f, \"rawT\":\"%s\", \"rawH\":\"%s\"}",
		    time(0),
		    temperature.val/5.0*9.0+32, humidity.val,
		    formatBuf(temperature.buf, temp_out_buf),
		    formatBuf(humidity.buf, humid_out_buf));
	
	return 0;
}
