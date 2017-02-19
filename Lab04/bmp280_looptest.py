#!/usr/bin/python
import time
import simplejson as json
import pprint
from bmp280 import PiBMP280

# create an instance of my pi bmp280 sensor object
sensor = PiBMP280(0x76)

print('Looping BMP280 ID Test for I2C Checking (Ctrl-C to stop)...')
counter = 0
while True:
    # Read the Sensor ID.
    (chip_id, chip_version) = sensor.readBMP280ID()
    print "      Count :", counter
    print "    Chip ID :", chip_id
    print "    Version :", chip_version
    print ""
    counter += 1
    time.sleep(0.5)
