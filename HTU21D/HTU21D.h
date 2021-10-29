#ifndef _HTU21D_H_
#define _HTU21D_H_

#define   HTU21D_I2C_ADDR 0x40

#define   HTU21D_TEMP     0xF3
#define   HTU21D_HUMID    0xF5

// struct to encapsulate raw and processed values
typedef struct {
	double		val;	// processed result
	unsigned char	buf[4];	// raw reading
} result;

// Get temperature
result getTemperature(int fd);

// Get humidity
result getHumidity(int fd);

#endif
