import requests
import json

def retrieve_message(object_id):
    url = "http://localhost:5000/obj"  
    headers = {'Content-Type': 'application/json'}
    payload = {'object_id': object_id}
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code == 200:
        print("Retrieved message:", response.json().get('message'))
    else:
        print("Error:", response.json().get('error', 'No error message returned'))

if __name__ == "__main__":
    object_id = input("Enter the object ID to retrieve: ")
    retrieve_message(object_id)
