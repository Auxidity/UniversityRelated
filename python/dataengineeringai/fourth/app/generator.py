
import requests
import json
import time
import random

BASE_URL = "http://flask:5000"  # Flask server URL


def wait_for_service():
    while True:
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("Flask service is up!")
                break
        except requests.ConnectionError:
            print("Waiting for Flask service to start...")
        time.sleep(1)

wait_for_service()
while True:
    # Get the current second
    current_time = time.time()
    timestamp = int(current_time)
    current_second = int(time.localtime(current_time).tm_sec)

    # Generate random data
    data = {
        "timestamp": timestamp,
        "timeofmeasurement": {
            "day": random.randint(1, 30),
            "month": random.randint(1, 12)
        },
        "temperature": random.uniform(-40, 40),
        "humidity": random.uniform(0, 100)
    }

    # Send to the appropriate endpoint
    if current_second % 2 == 0:  # Even second
        response = requests.post(f"{BASE_URL}/even", json=data)
    else:  # Odd second
        response = requests.post(f"{BASE_URL}/odd", json=data)

    print(f"Sent data: {data}, Response: {response.status_code}")

    # Wait for 1 second before generating the next data
    time.sleep(1)
