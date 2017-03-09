#!/usr/bin/python
import time
import paho.mqtt.client as paho
import json
import ast

localBroker = "iot82dd"     # Local MQTT broker
localPort   = 1883          # Local MQTT port
localUser   = "pi"          # Local MQTT user
localPass = "raspberry"     # Local MQTT password
localTopic = "iot/sensor"   # Local MQTT topic to monitor
cloudTopic = "iot/azure"    # publish to simulated Azure topic 
localTimeOut = 120          # Local MQTT session timeout


# The callback for when a CONNACK message is received from the broker.
def on_connect(client, userdata, flags, rc):
    print("CONNACK received with code %d." % (rc))
    mqttc.subscribe(localTopic, 0)


def on_message(mosq, obj, msg):
    global message
    print("Topic Rx:" + msg.topic + " QoS:" + str(msg.qos) + "\n")
    clean_json = ast.literal_eval(msg.payload)
    print ("Payload: ")
    # import pdb; pdb.set_trace()
    print json.dumps(clean_json , indent=4, sort_keys=True)
    # message = msg.payload
    # This is where we will develop client connect to  Azure IoT Suite
    mqttc.publish(cloudTopic,msg.payload, 1);


print('Establish MQTT Broker Connection')
# Setup to listen on topic`
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(localUser, localPass) ## added as bug fix because of timeouts
mqttc.connect(localBroker, localPort, localTimeOut)
print('MQTT Listener Loop <ctl-C> to break...')
mqttc.loop_forever()

