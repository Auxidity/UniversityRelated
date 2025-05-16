"""
File     : mqtt_sub.py
Author   : Daniel Kortesmaa
Desc.    : Automated mqtt subscriber launcher. Expand functionality on received messages, and pass it to flask (Look into using FastAPI instead more. Might be overkill)
"""

import paho.mqtt.client as mqtt
import os

#Using a file as a signal handler. Is created with speech module on ctrl+c, and then deleted after by this script.
TERMINATION_SIGNAL_FILE = "terminate_mqtt.txt"

#Ensure there is no ghost file on startup
if os.path.exists(TERMINATION_SIGNAL_FILE):
            os.remove(TERMINATION_SIGNAL_FILE)

# Keywords for future API calls to detect from speech
keywords = ["yes", "no", "mom", "reddit"]

#List to store received messages, in case multiple keywords are needed.
received_messages = []

def on_message(client, userdata, msg):
    global received_messages
    message = msg.payload.decode()
    if message != "":
        print(f"Received message: {msg.payload.decode()}")
        
        #Store the messages to memory in case multiple keywords are neccesary.
        received_messages.append(message)
        check_keywords(message)

def check_keywords(message):
    global received_messages

    """
    Change the actions as appropriate API calls based on keywords. Probably smartest approach is to 
    create a FSM that is being driven by actions, and this original list is for initial state control.
    Further actions inside each state for more detailed actions.
    Potentially could use AI to enhance accuracy of keyword detection, albeit it does increase lag.
    Partial inclusion of AI at certain steps is also an option.
    """
    actions = {
        ("yes", "mom"): lambda: print("Keyword yes & mom found!"),
        ("no", "reddit"): lambda: print("Keyword no & reddit found!"),
    }

    # Check for each specific combination of keywords
    for key_combination, action in actions.items():
        if all(keyword in " ".join(received_messages) for keyword in key_combination):
            action()
            received_messages = []  # Empty the list
            return

    # Count the number of keywords found in the message. Arbitrary function right now.
    num_keywords_found = sum(1 for keyword in keywords if keyword in message)
    if num_keywords_found > 0:
        print(f"{num_keywords_found} keyword(s) detected!")

    # Check if the total number of keywords found is greater than or equal to 5. Arbitrary function right now
    total_keywords_found = sum(1 for msg in received_messages for keyword in keywords if keyword in msg)
    if total_keywords_found >= 5:
        print(" ".join(received_messages))  # Print all received messages
        received_messages = []  # Clear the list



def main():
    mqtt_broker = "localhost"
    mqtt_topic = "tmp/topic"

    # Create an MQTT client instance
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    # Set the callback function for incoming messages
    mqtt_client.on_message = on_message

    # Connect to the MQTT broker
    mqtt_client.connect(mqtt_broker, 1883)

    # Subscribe to the topic
    mqtt_client.subscribe(mqtt_topic)

    #Start mqtt client loop in a separate thread
    mqtt_client.loop_start()

    try:
        #Empty loop to keep the separate thread alive
        #Signal for the subscriber to stop listening once the file exists
        while not os.path.exists(TERMINATION_SIGNAL_FILE):
            pass
    
    except KeyboardInterrupt:
         #No need to do kill condition cleanup, from exception straight to finally block.
         print("\nLocal keyboard interrupt detected") 

    finally:
        #Kill condition cleanup
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        #Remove the file so that you can run the script again
        if os.path.exists(TERMINATION_SIGNAL_FILE):
            os.remove(TERMINATION_SIGNAL_FILE)
        print("Exiting")


if __name__ == "__main__":
    main()
