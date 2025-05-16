import gpiod
import json
import paho.mqtt.client as mqtt
import subprocess

GPIO_CHIP = "gpiochip0"
LED_LINE = 22

MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "sensors/test"
DESIRED_MAC = "C8:85:45:28:6B:DE"

#C8:85:45:28:6B:DE
# Callback function to handle MQTT messages
def on_message(client, userdata, message):
    try:
        # Decode and parse the incoming JSON message
        data = json.loads(message.payload.decode())
        device_mac = data.get("mac", "").upper()

        if device_mac == DESIRED_MAC:
            acceleration_z = data.get("data_acceleration_z", 0)
            # Control GPIO based on acceleration_z value
            if acceleration_z >= 0:
                set_gpio_value(0)  # Set GPIO to 0
            else:
                set_gpio_value(1)  # Set GPIO to 1
        


    except Exception as e:
        print("Error processing MQTT message:", str(e))

def set_gpio_value(value):
    try:
        subprocess.run(['gpioset', GPIO_CHIP, f"{LED_LINE}={value}"])

    except subprocess.CalledProcessError as e:
        print("Error:", e)

# Create MQTT client
client = mqtt.Client()
client.on_message = on_message

# Connect to MQTT broker and subscribe to topic
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop
client.loop_forever()
