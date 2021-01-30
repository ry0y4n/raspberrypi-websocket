#!/usr/bin/env python3

import wiringpi as wp
import time
import RPi.GPIO as GPIO

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

GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
gp_out = 4
GPIO.setup(gp_out, GPIO.OUT)
motor = GPIO.PWM(gp_out, 50)
motor.start(0.0)

flag = True

while True:
    buffer = 0x6800
    buffer = buffer.to_bytes(2,byteorder='big')
    wp.wiringPiSPIDataRW(SPI_CH, buffer)
    value = (buffer[0]*256+buffer[1]) & 0x3ff
    print(value)
    if value > THRESHOLD:
      print(value)
      time.sleep(0.2)

      bot = 2.5
      mid = 7.2
      top = 12.0

      if flag:
        motor.ChangeDutyCycle(4.0)
        flag = not flag
        print(flag)
      else:
        motor.ChangeDutyCycle(5.5)
        flag = not flag
        print(flag)

      time.sleep(0.5)


    time.sleep(1)

GPIO.cleanup()
