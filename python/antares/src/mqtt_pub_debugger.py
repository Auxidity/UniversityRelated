"""
File     : mqtt_pub_debugger.py
Author   : Daniel Kortesmaa
Desc.    : Publisher script to test functionality using mqtt messages that dont come from SR. Needs to be ran from terminal. Use mqtt_sub to track messages only.
"""

import paho.mqtt.client as mqtt
import threading

# MQTT Broker (localhost)
broker_address = "localhost"
broker_port = 1883

# MQTT Topic
topic = "tmp/topic"

# Callback function to handle MQTT connection
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code "+str(rc))

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect

# Connect to MQTT broker
client.connect(broker_address, broker_port, 60)



def main():
    while True:
        message = input("Enter message to publish (type 'exit' to quit): ")
        if message.lower() == 'exit':
            client.disconnect()
            break
        # Publish message to MQTT topic
        client.publish(topic, message)
        print("Message published to topic '{}'".format(topic))

input_thread = threading.Thread(target=main)
input_thread.start()

client.loop_forever()

input_thread.join()
