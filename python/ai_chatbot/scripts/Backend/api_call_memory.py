"""
File : alt_api_call.py
Author : Daniel Kortesmaa
Description : Third iteration of api_call.py. Uses json payloads to communicate with openai api. Old messages will get appended to payload.
"""
#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import requests
import json

def openai_api_call(conversation):
    # api_key = REDACTED, use your own key
    # URL = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": conversation,
        "temperature": 1.0,
        "top_p": 1.0,
        "n": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False)

    # Ensure the request was successful (status code 200)
    if response.status_code == 200:
        # Decode bytes to string and load JSON
        response_str = response.content.decode('utf-8')
        json_data = json.loads(response_str)

        # Extract content from the response
        content = json_data['choices'][0]['message']['content']

        # Return the content
        return content
    else:
        #print(f"Error: {response.status_code}, {response.text}") debug line
        return response.status_code


