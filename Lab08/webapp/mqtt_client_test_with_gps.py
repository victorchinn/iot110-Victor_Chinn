#!/usr/bin/python
import time
import socket
import paho.mqtt.client as paho
from sense import PiSenseHat

# add the GPS MEASUREMENTS of lat,lon,altitude,# of satellites in view to the payload 

#myHostname = 'iot8e3c'

myHostname = 'iot82dd'

localBroker = "iot82dd"     # Local MQTT broker
localPort   = 1883          # Local MQTT port
localUser   = "pi"          # Local MQTT user
localPass = "raspberry"     # Local MQTT password
localTopic = "iot/sensor"   # Local MQTT topic to monitor
localTimeOut = 120          # Local MQTT session timeout

# The callback for when a CONNACK message is received from the broker.
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

# The callback for when a PUBLISH message is received from the broker.
def on_message(client, userdata, msg):
    print (string.split(msg.payload))

# display one row of blue LEDs (just for fun)
def displayLine(row):
    blue = (0, 0, 255)
    for i in range(0,8):
        x = i % 8
        y = (i / 8) + row
        # print("set pixel x:%d y:%d" % (x,y))
        pi_sense.set_pixel(x,y,blue)
        time.sleep(0.02)


# Create a sense-hat object
pi_sense = PiSenseHat()
print('PI SenseHat Object Created')

# Get hostname
## Get my machine hostname
# import pdb; pdb.set_trace()
if socket.gethostname().find('.') >= 0:
    hostname=socket.gethostname()
else:
    hostname=socket.gethostbyaddr(socket.gethostname())[0]

# Setup to Publish Sensor Data
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(localBroker, localPort, localTimeOut)

# initialize message dictionary
msg = {'topic':localTopic, 'payload':"", 'qos':0, 'retain':False }

pi_sense.clear_display()

# loop
print('Getting Sensor Data')
for i in range(1,9):
    print("SensorSet[%d]" % (i))
    displayLine(i-1)
    sensors = pi_sense.getAllSensors()

    sensors['host'] = hostname

    # add the GPS Sensor Measurements here ...
    lat = 0
    lon = 0
    alt = 0 
    numsats = 0 

    sensors['location']['lat'] = { 'value':lat, 'dir':'N'}
    sensors['location']['lon'] = { 'value':lon, 'dir':'E'}
    sensors['location']['alt'] = { 'value':alt, 'unit':'feet'}
    sensors['location']['sats'] = { 'value':numsats}
    # end add for GPS

    msg['payload'] = str(sensors)
    print("msg["+str(i)+"]:"+msg['payload'])

#   publish(topic, payload=None, qos=0, retain=False)
    mqttc.publish('iot/sensor', msg['payload'], 1)
    time.sleep(2.0)

pi_sense.clear_display()
print('End of MQTT Messages')
quit()