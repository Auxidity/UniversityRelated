"""
File : yamlifier.py
Author : Daniel Kortesmaa
Description : makes an api call using the output of tertiary_data_processing.py files and creates yaml files out of them using chatgpt.
"""

import requests
import json, os, shutil

# Get the parent directory of the script's directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
data_dir = os.path.join(parent_dir, 'data/processed')
yaml_dir = os.path.join(parent_dir, 'data/yaml')
# Create the YAML directory if it doesn't exist
if not os.path.exists(yaml_dir):
    os.makedirs(yaml_dir)

def openai_api_call(message_content):
    # api_key = REDACTED
    # URL = "https://api.openai.com/v1/chat/completions"

    yaml_content = """
version: "2.0"

nlu:
- intent: New_study_reveals_how_protest_tactics_impact_public_support_for_Black_Lives_Matter
  examples: |
    - I think support was also lost after learning where much of the money being donated to BLM was going.
    - Let's all just pretend the "summer of love" didn't happen.
    - I support the tactics of rooftop koreans.
    - Damn, so white conservatives think peaceful protests are the same as riots when it's the African-Americans doing it.
    - The amount of neo-terms within this article is wild. Inventing language to get to the finish line.
    - Seeing that guy bleeding to death from a gunshot to the gut while trying to protect his small business from looting while crying for help and the protesters are just walking over his body and pool of blood ignoring him while he cried for help and died was what led me to lose support.

- intent: Origins_of_Black_Lives_Matter_movement
  examples: |
    - Unfortunately they weren't even the originators of the Black Lives Matter movement.
    - BLM is not itself a central organization. It's a decentralized movement.
    - It's first act of surrounding the police station with people inside shouting "burn it down" then they have to burst through a chain link fence.

- intent: White_conservatives_and_protest_tactics
  examples: |
    - Isn't the inverse also shown by the authors too?
    - So disruptive protests alienate potential allies vs peaceful protests? That seems like an important takeaway.
    - Disruptive protests alienate people with implicit bias against the protesters.
    - Because people love hearing things that confirm their biases.
    - They also thunk January 6th was a peaceful protest by average tourist.

- intent: Study_insights_on_protest_tactics_and_public_support
  examples: |
    - Can you relate what you claim to the actual research?
    - No numbers in the entire article except the sample size of 3000.
    - Even then, the majority of the sample size was democratic.
    - Look at the first act of the riots which was to surround a police station and burn it down.
    - Destroying cities is not peaceful that's the thing.

responses:
  New_study_reveals_how_protest_tactics_impact_public_support_for_Black_Lives_Matter:
    - Unfortunately they weren't even the originators of the Black Lives Matter movement. They just capitalized off of other black people's pain.
    - BLM is not itself a central organization. It's a decentralized movement.
    - Seeing that guy bleeding to death from a gunshot to the gut while trying to protect his small business from looting while crying for help and the protesters are just walking over his body and pool of blood ignoring him while he cried for help and died was what led me to lose support.
  White_conservatives_and_protest_tactics:
    - Isn't the inverse also shown by the authors too?
    - I think the key here is that when you support a cause you are more forgiving of the means of protest and vice verse.
    - The researchers uncovered that whites' reactions to the protests were influenced by their levels of racial resentment.
    - White conservatives make no distinction between activities at the low and high end of the protest disruption spectrum when it comes to Black Lives Matter protests.
    - Disruptive protests alienate potential allies vs peaceful protests? That seems like an important takeaway.
    - White respondents with lower levels of racial resentment were more likely to view disruptive protests negatively.
  Study_insights_on_protest_tactics_and_public_support:
    - Can you relate what you claim to the actual research?
    - The researchers uncovered that whites' reactions to the protests were influenced by their levels of racial resentment.
    - White conservatives make no distinction between activities at the low and high end of the protest disruption spectrum when it comes to Black Lives Matter protests.
    - White respondents with lower levels of racial resentment were more likely to view disruptive protests negatively.
    - Even then, the majority of the sample size was democratic.
    - Destroying cities is not peaceful that's the thing.
"""
    system_content = "You are to create yaml training data for RASA chatbot out of the provided JSON data that can be directly be written as yaml files. Content inside response field are a direct response to the 'comment', and the topic that is being discussed is under title field. Structure the data comprehensively, including both intents and responses. Don't forget to include the original topic as an intent aswell but do not create duplicate intents. Do not use U+2019 character, and use ' instead. The following is an example of the format to use when creating the training data, make it exactly in the same format and check that what you have created is strictly in same format : \
        "
    system_content += yaml_content

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role":"system", "content": system_content},
            {"role": "user", "content": message_content}
            ],
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

def write_to_file(content, file_name):
    with open(file_name, "w") as file:
        file.write(content)

file_names = os.listdir(data_dir)
for file_name in file_names:
    # Check if the file is a JSON file
    if file_name.endswith('.json'):
        # Construct the full path to the file
        json_file_path = os.path.join(data_dir, file_name)
        
        # Load the JSON data from the file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            data_str = json.dumps(data)
            response = openai_api_call(data_str)

            yaml_filename = os.path.splitext(file_name)[0] + ".yaml"
            yaml_file_path = os.path.join(yaml_dir, yaml_filename)
            with open(yaml_file_path, "w") as file:
                file.write(response)

#Delete contents of processed dir at end so you don't api call old data. Comment out to preserve the jsons for inspection.
if os.path.exists(data_dir):
    shutil.rmtree(data_dir)
