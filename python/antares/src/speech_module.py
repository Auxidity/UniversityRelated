"""
File     :  speech_recognition.py
Author   :  Daniel Kortesmaa
Desc.    :  Speech recognition module. Creates a thread that handles speech recognition separately, and
            publishes the interpreted message on mqtt. On Ctrl+C, kills thread & subscriber.
"""

"""
Notes:

the is_running in SpeechRecognitionThread is potentially redundant. If there is a better way to handle than the current one,
I might go back to it but Im heavily considering removing it altogether and using thread.join() in its stead.
"""

import os
import pyaudio
from vosk import Model, KaldiRecognizer
import json
import threading
import paho.mqtt.client as mqtt
import time

#Signal processing testing libraries. Audio conversions mess with the recognizer, needs more research.
"""
import numpy as np
import librosa
import noisereduce
"""
#IPC signal to handle speech_module from FSM
FSM_KILLSWITCH = "src/killswitch.txt"

#IPC signal for handling processes to gracefully kill processes when this module gets killed.
TERMINATION_SIGNAL_FILE = "src/terminate_mqtt.txt" #Edit based on where you run this from. If you run directly from terminal, change to just terminate_mqtt.txt. From vscode, src/terminate_mqtt.txt.

#IPC signal for controlling the thread state to save resources. When an API call is decided on, kill the mic thread until API call finishes & relaunch the thread.
THREAD_SIGNAL_FILE = "src/thread_alive.txt"

class SpeechRecognitionThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.model_path = "model"  # Edit as necessary
        self.mqtt_broker = "localhost"  # Update with your MQTT broker details
        self.mqtt_topic = "tmp/topic"  # Update with your MQTT topic
        self.running = False
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqtt_client.on_message = self.on_message

    def run(self):
        self.mqtt_client.connect(self.mqtt_broker, 1883)
        self.mqtt_client.subscribe(self.mqtt_topic)
        self.running = True

        # Redirect stderr to /dev/null or nul to hide alsa lib errors on default runtime.
        save_stderr = os.dup(2)
        os.close(2)
        os.open(os.devnull, os.O_WRONLY)

        #Model not found error
        if not os.path.exists(self.model_path):
            print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            return

        model = Model(self.model_path)
        recognizer = KaldiRecognizer(model, 16000)
        recognizer.SetPartialWords(1)

        CHUNK = 4000
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Listening...")

        while self.running:
            data = stream.read(CHUNK)

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_dict = json.loads(result)

                if "text" in result_dict:
                    words = result_dict["text"].split()
                    output_text = ' '.join(word for word in words)
                    self.mqtt_client.publish(self.mqtt_topic, output_text)  # Publish to MQTT topic

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Restore stdout and stderr
        os.dup2(save_stderr, 2)
        os.close(save_stderr)

    def stop(self):
        self.running = False

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        if message == "start":
            if not self.running:
                self.start()
        elif message == "stop":
            self.stop()


def main():
    if os.path.exists(TERMINATION_SIGNAL_FILE):
            os.remove(TERMINATION_SIGNAL_FILE) #Cleanup
    
    if os.path.exists(FSM_KILLSWITCH): 
        os.remove(FSM_KILLSWITCH) #Initialization killswitch for thread

    mqtt_broker = "localhost" #Localhost for now
    mqtt_topic = "tmp/topic"

    # Connect to the MQTT broker inside the while loop. Specify the client outside, connections inside
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    speech_recognition_thread = None #Initialization

    try:
        while not os.path.exists(FSM_KILLSWITCH):
            if os.path.exists(THREAD_SIGNAL_FILE):
                if speech_recognition_thread is None:
                    speech_recognition_thread = SpeechRecognitionThread()
                    speech_recognition_thread.start()
                    mqtt_client.connect(mqtt_broker, 1883)
                    mqtt_client.subscribe(mqtt_topic)
                    mqtt_client.on_message = speech_recognition_thread.on_message

            else:
                if speech_recognition_thread is not None:
                    speech_recognition_thread.stop()
                    speech_recognition_thread.join()
                    mqtt_client.disconnect()
                    speech_recognition_thread = None
                continue
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        # If KeyboardInterrupt (Ctrl+C) is received, Kill the script entirely. Cleanup of resources
        speech_recognition_thread.stop()
        speech_recognition_thread.join()
        mqtt_client.disconnect()
        open(TERMINATION_SIGNAL_FILE, 'w').close() #Kills the subscriber script. File is then deleted on subscriber scripts end to ensure that it gets to read it.
        speech_recognition_thread = None
        print()

    finally:
        # Final cleanup in case this is reached unexpectedly
        if speech_recognition_thread is not None:
            speech_recognition_thread.stop()
            speech_recognition_thread.join()
            
        if mqtt_client.is_connected():
            mqtt_client.disconnect()

        open(TERMINATION_SIGNAL_FILE, 'w').close() #Kills the subscriber script. File is then deleted on subscriber scripts end
        if os.path.exists(FSM_KILLSWITCH): #Thread killswitch cleanup
            os.remove(FSM_KILLSWITCH)
        print()




if __name__ == "__main__":
    main()