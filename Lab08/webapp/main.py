#!/usr/bin/python
import time
import datetime
from sense import PiSenseHat
import paho.mqtt.client as paho
from flask import *

# create Pi SenseHat Object
pi_sense_hat = PiSenseHat()

# ============================== Functions ====================================
def get_sensor_values():
    return pi_sense_hat.getAllSensors()

# ============================= MQTT Callbacks ================================
# The callback for when a CONNACK message is received from the broker.
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))

# The callback for when a PUBLISH message is received from the broker.
def on_message(client, userdata, msg):
    print (string.split(msg.payload))
# ============================= MQTT Callbacks ================================

# MQTT Configuration for local network
localBroker = "iot82dd"     # Local MQTT broker
localPort   = 1883          # Local MQTT port
localUser   = "pi"          # Local MQTT user
localPass = "raspberry"     # Local MQTT password
localTopic = "iot/sensor"   # Local MQTT topic to monitor
localTimeOut = 120          # Local MQTT session timeout

# Setup to Publish Sensor Data
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(localBroker, localPort, localTimeOut)

# ============================== API Routes ===================================
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

# =========================== Endpoint: /myData ===============================
# read the sensor values by GET method from curl for example
# curl http://iot8e3c:5000/myData
# -----------------------------------------------------------------------------
@app.route('/myData')
def myData():
    def get_values():
        while True:
            # return the yield results on each loop, but never exits while loop
            data_payload = get_sensor_values()
            yield('data: {0}\n\n'.format(data_payload))
            print("MQTT Topic:"+localTopic, str(data_payload))
            mqttc.publish(localTopic,str(data_payload))
            time.sleep(2.0)
    return Response(get_values(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
