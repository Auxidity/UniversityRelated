"""
File     :  mqtt_broker.py
Author   :  Daniel Kortesmaa
Desc.    :  mqtt broker script placeholder. Sole purpose is to launch mosquitto service. Following is normal
            in case the service is already enabled. In such case no need for further actions, just run \
            speech_module & mqtt_sub.

            1710772071: Opening ipv4 listen socket on port 1883.
            1710772071: Error: Address already in use
            1710772071: Opening ipv6 listen socket on port 1883.
            1710772071: Error: Address already in use                                                   \
            
            Potential extension is to create custom configuration settings using this script to avoid system
            configurations. For non-localhost connections (Raspberry - PC - Android(?))
"""

import subprocess
import time

def start_mosquitto():
    # Start Mosquitto server as a subprocess
    mosquitto_process = subprocess.Popen(["mosquitto", "-v"])

    return mosquitto_process

def stop_mosquitto(mosquitto_process):
    # Terminate the Mosquitto server subprocess
    mosquitto_process.terminate()
    mosquitto_process.wait()

def main():
    try:
        # Start Mosquitto server
        mosquitto_process = start_mosquitto()
        print("Mosquitto server started. Press Ctrl+C to terminate.")

        # Wait indefinitely until KeyboardInterrupt
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # KeyboardInterrupt to stop Mosquitto server
        print()
        print("Terminating Mosquitto server...")
        stop_mosquitto(mosquitto_process)
        print("Mosquitto server terminated.")

if __name__ == "__main__":
    main()
