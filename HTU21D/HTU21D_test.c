#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "wiringPi.h"
#include "wiringPiI2C.h"

#include "HTU21D.h"

int main ()
{
	int fd = wiringPiI2CSetup(HTU21D_I2C_ADDR);
	if ( 0 > fd )
	{
		fprintf (stderr, "Unable to open I2C device: %s\n", strerror (errno));
		exit (-1);
	}
	
	for(;;) {
		printf("%5.2f°F %5.2f%%\n",
                getTemperature(fd).val/5.0*9.0+32,
                getHumidity(fd).val);
		usleep(10);
	}
	
	return 0;
}
