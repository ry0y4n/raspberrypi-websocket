#!/usr/bin/env python3

import wiringpi as wp
import time

# SPI channel (0 or 1)
SPI_CH = 0

# SPI speed (hz)
SPI_SPEED = 1000000

# GPIO number
LED_PIN = 25

# threshold
THRESHOLD = 200

# setup
wp.wiringPiSPISetup (SPI_CH, SPI_SPEED)
wp.wiringPiSetupGpio()
wp.pinMode(LED_PIN, wp.GPIO.OUTPUT)

while True:
    buffer = 0x6800
    buffer = buffer.to_bytes(2,byteorder='big')
    wp.wiringPiSPIDataRW(SPI_CH, buffer)
    value = (buffer[0]*256+buffer[1]) & 0x3ff
    print (value)

    if value > THRESHOLD:
      print(value)
      time.sleep(0.2)

    time.sleep(1)
