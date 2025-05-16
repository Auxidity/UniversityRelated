"""
File : caller.py
Author : Daniel Kortesmaa
Description : Caller, handles a lot of data fetching, stt module fetching etc.
"""
#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import subprocess
import os
from alt_api_call import openai_api_call
from stt import recognize_speech
import json

class FilePathError(Exception):
    pass

def get_f_path():
    # Get the absolute path of the directory containing caller.py
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to stt.py & tts.py
    stt_path = os.path.join(current_script_dir, 'stt.py')
    tts_path = os.path.join(current_script_dir, 'tts.py')
    json_path = os.path.join(current_script_dir,'config.json')
    led_path = os.path.join(current_script_dir, 'leds.py')

    if not os.path.exists(stt_path):
        raise FilePathError(f"Error 4: File path on STT")
    
    if not os.path.exists(json_path):
        raise FilePathError(f"Error 4: File path on JSON")
    
    if not os.path.exists(tts_path):
        raise FilePathError(f"Error 4: File path on TTS")
    
    if not os.path.exists(led_path):
        raise FilePathError(f"Error 4: File path on LED control")
    

    return  tts_path, json_path, stt_path, led_path

def config_fetcher(file_path, target_id):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except json.JSONDecodeError:
        return f"Invalid JSON format in file: {file_path}"

    #print("Loaded data:", data)  # Add this line for debugging

    for entry in data:
        if entry.get("id") == target_id:
            return entry.get("content")
    return None  # Return None if the ID is not found

def config():
    while True:
                id = input("ID: ")
                _, json_path, _, _ = get_f_path() #Underscore eats the undesired path 1 return from function (in this specific function call only undesired).
                chatgpt_config = config_fetcher(json_path, id)
                if chatgpt_config is not None:
                    return chatgpt_config
                    
                else:
                    print("Invalid ID")


def append_config(json_file, new_entry):
    # Load existing data from JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Check if ID already exists
    ids = [entry['id'] for entry in data]
    if new_entry['id'] not in ids:
        # Append new entry if ID is not a duplicate
        data.append(new_entry)
        # Write updated data back to JSON file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        return f"New entry {new_entry} appended successfully!"
    else:
        return "ID already exists, entry not appended."

def create_entry(new_id, new_content):
    #Expand this later with all configs, temp etc
    new_entry = {"id": new_id, "content": new_content}
    return new_entry

def remove_entry(json_file, entry_id):
    # Load existing data from JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Find the index of the entry with the given ID
    index_to_remove = None
    for i, entry in enumerate(data):
        if entry['id'] == entry_id:
            index_to_remove = i
            break
    
    # Remove the entry if found
    if index_to_remove is not None:
        del data[index_to_remove]
        # Write updated data back to JSON file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        return "Entry with ID {} removed successfully.".format(entry_id)
    else:
        return "Entry with ID {} not found.".format(entry_id)

def main(ip_main, lang_tts, lang_stt, id, default_color):
    tts_lang = lang_tts
    stt_lang = lang_stt
    tts_path, _, _, led_path = get_f_path()
    ip = ip_main
    color = default_color
    api_config = id
    #print(api_config) #Debug
    #print(output) #Debug


    #Set eyes to specified color color. Hardcoded for now
    subprocess.Popen(['python2', led_path, ip, "red"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    output = recognize_speech(stt_lang) #STT Call
   
    if output != 2:
        #Succesfully ran stt
            try:
                # Attempt to call api_call without checking returncode
                api_output = openai_api_call(output, api_config)
                print("Output from api_call.py: ", api_output)


                # Run tts.py as a subprocess, passing api_output as an argument
                #print(ip)#Debug line
                process_tts = subprocess.Popen(['python2', tts_path, api_output, ip, tts_lang], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output_tts, errors_tts = process_tts.communicate()

                if output_tts is not None:
                    # Print the output or error message from tts.py
                    output_text_tts = output_tts.strip()
                    print("Output from tts.py: \n",output_text_tts)
                    return 0
                else:
                     print("Error in tts.py: ", errors_tts)
            except Exception as api_error:
                print(api_error)
    else:
        return output

    #Set eyes back to default
    subprocess.Popen(['python2', led_path, ip, color], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)



if __name__ == "__main__":
    main()
