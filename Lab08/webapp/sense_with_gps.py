#!/usr/bin/python
# =============================================================================
#        File : sense_with_gps.py
# Description : Driver interface for SenseHat Module
#      Author : S. Dame/Victor Chinn
#        Date : 2/13/2017
# =============================================================================
#
#  Official sense-hat API available from :
#  http://pythonhosted.org/sense-hat/api/
#
# add support for GPS module
#
# =============================================================================
from sense_hat import SenseHat

class PiSenseHat(object):
    """Raspberry Pi 'IoT Sense Hat API Driver Class'."""

    # Constructor
    def __init__(self):
        self.sense = SenseHat()
        # enable all IMU functions
        self.sense.set_imu_config(True, True, True)

    # pixel display
    def set_pixel(self,x,y,color):
    # red = (255, 0, 0)
    # green = (0, 255, 0)
    # blue = (0, 0, 255)
        self.sense.set_pixel(x, y, color)

    # clear pixel display
    def clear_display(self):
        self.sense.clear()

    # Pressure
    def getPressure(self):
        return self.sense.get_pressure()

    # Temperature
    def getTemperature(self):
        return self.sense.get_temperature()

    # Humidity
    def getHumidity(self):
        return self.sense.get_humidity()

    def getHumidityTemperature(self):
        return self.sense.get_temperature_from_humidity()

    def getPressureTemperature(self):
        return self.sense.get_temperature_from_pressure()

    def getOrientationRadians(self):
        return self.sense.get_orientation_radians()

    def getOrientationDegrees(self):
        return self.sense.get_orientation_degrees()

    # degrees from North
    def getCompass(self):
        return self.sense.get_compass()

    def getAccelerometer(self):
        return self.sense.get_accelerometer_raw()

    def getEnvironmental(self):
        sensors = {'name' : 'sense-hat', 'environmental':{}}
        return sensors

    def getJoystick(self):
        sensors = {'name' : 'sense-hat', 'joystick':{}}
        return sensors

    def getInertial(self):
        sensors = {'name' : 'sense-hat', 'inertial':{}}

    def getAllSensors(self):
        sensors = {'name' : 'sense-hat', 'environmental':{}, 'inertial':{}, 'joystick':{}, 'location':{}}  # add location
        sensors['environmental']['pressure'] = { 'value':self.sense.get_pressure(), 'unit':'mbar'}
        sensors['environmental']['temperature'] = { 'value':self.sense.get_temperature(), 'unit':'C'}
        sensors['environmental']['humidity'] = { 'value':self.sense.get_humidity(), 'unit': '%RH'}
        accel = self.sense.get_accelerometer_raw()
        sensors['inertial']['accelerometer'] = { 'x':accel['x'], 'y':accel['y'], 'z': accel['z'], 'unit':'g'}
        orientation = self.sense.get_orientation_degrees()
        sensors['inertial']['orientation'] = { 'compass':self.sense.get_compass(), 'pitch':orientation['pitch'], 'roll':orientation['roll'], 'yaw': orientation['yaw'], 'unit':'degrees'}
        
        sensors['location']['lat'] = { 'value':0, 'dir':'N'}
        sensors['location']['lon'] = { 'value':0, 'dir':'N'}
        sensors['location']['alt'] = { 'value':0, 'unit':'feet'}
        sensors['location']['sats'] = { 'value':0}

        return sensors
# =============================================================================
# main to test from CLI
def main():

    # create an instance of my pi sense-hat sensor object
    pi_sense_hat = PiSenseHat()

    # Read Parameters.
    p = pi_sense_hat.getPressure()
    t_c = pi_sense_hat.getTemperature()
    h = pi_sense_hat.getHumidity()
    ht = pi_sense_hat.getHumidityTemperature()
    hp = pi_sense_hat.getPressureTemperature()
    orientation = pi_sense_hat.getOrientationDegrees()
    accel = pi_sense_hat.getAccelerometer()
    d = pi_sense_hat.getCompass()

    print("================ Discrete Sensor Values ==================")
    print "      Pressure :", p
    print "   Temperature :", t_c
    print "      Humidity :", h
    print "  HumidityTemp :", ht
    print "  PressureTemp :", hp
    print "       Compass :", d
    print("  p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
    print("  x: {x}, y: {y}, z: {z}".format(**accel))
    print("==========================================================\n")

    print("================== Dictionary Object =====================")
    print(pi_sense_hat.getAllSensors())
    print("==========================================================\n")

if __name__=="__main__":
   main()
