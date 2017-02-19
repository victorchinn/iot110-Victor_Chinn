#!/usr/bin/python
import pprint
from bmp280 import PiBMP280

# create an array of my pi bmp280 sensor dictionaries
sensor = []
sensor.append({'name' : 'bmp280', 'addr' : 0x76, 'chip' : PiBMP280(0x76) , 'data' : {}})

# Read the Sensor ID for 0x76 -> values into the ['data'] dictionary
(chip_id, chip_version) = sensor[0]['chip'].readBMP280ID()
sensor[0]['data']['chip_id'] = chip_id
sensor[0]['data']['chip_version'] = chip_version

print "  ============================== SENSOR   =============================="
print "  Chip ADDR :", hex(sensor[0]['addr'])
print "    Chip ID :", sensor[0]['data']['chip_id']
print "    Version :", sensor[0]['data']['chip_version']

# Read the Sensor Temp/Pressure values into the ['data'] dictionary
(temperature, pressure) = sensor[0]['chip'].readBMP280All()
sensor[0]['data']['temperature'] = { 'reading': temperature, 'units' : 'C' }
sensor[0]['data']['pressure'] = { 'reading': pressure, 'units' : 'hPa' }

print "Temperature :", sensor[0]['data']['temperature']['reading'], "C"
print "   Pressure :", sensor[0]['data']['pressure']['reading'] , "hPa"

pprint.pprint(sensor[0])
print "  ======================================================================"
