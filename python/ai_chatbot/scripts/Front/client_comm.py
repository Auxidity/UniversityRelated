"""
File : client_comm.py
Author : Daniel Kortesmaa
Description : gui commands to interact with server
"""
#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

class FilePathError(Exception):
    pass

import json
import sys
import tkinter as tk
from tkinter import filedialog
import os


def construct_server_kill():
    command = "0"
    ip = "1"
    config_id = "1"
    lang = "1"
    content = "1"
    content2 = "2"
    return command, ip, config_id, lang, content, content2

def construct_initial_payload_content():
    command = "1"
    ip = "1"
    config_id = "1"
    lang = "1"
    content = "1"
    content2 = "2"
    return command, ip, config_id, lang, content, content2

def command():
    command = input("Command: ")
    return command

def ip():
    ip = input("IP: ")
    return ip

def config_id():
    command = input("Config ID: ")
    return command

def language():
    command = input("Language: ")
    return command

def content():
    command = input("Content: ")
    return command

def alt_content():
    command = input("Alt_Content: ")
    return command

#Content is text string for file
def construct_payload(command, ip, config_id, lang, content=None, content2=None):
    
    if content is not None:
        payload = {
                "command": command,
                "ip": ip,
                "config_id": config_id,
                "lang": lang,
                "content": content,
                "alt_content": content2
            }
    else:
        payload = {
                "command": command,
                "ip": ip,
                "config_id": config_id,
                "lang": lang,
                "content": "1",
                "alt_content": "1"
            }


    return payload



def open_file(file_path):
    with open(file_path) as file:
        content = file.read()
        print(content)
        return content


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename()
    
    return file_path

def file_as_string():
    file = open_file_dialog()

    if file:
        text = open_file(file)
        
        return text
    else:
        
        return 1 #Error 1
    



""" Potentially neccesary code, these are caller functions but goal is to not have caller be inside the app.
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

def get_f_path():
    # Get the absolute path of the directory containing caller.py
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to stt.py & tts.py
    stt_path = os.path.join(current_script_dir, 'stt.py')
    tts_path = os.path.join(current_script_dir, 'tts.py')
    json_path = os.path.join(current_script_dir,'config.json')

    if not os.path.exists(stt_path):
        raise FilePathError(f"Error 4: File path on STT")
    
    if not os.path.exists(json_path):
        raise FilePathError(f"Error 4: File path on JSON")
    
    if not os.path.exists(tts_path):
        raise FilePathError(f"Error 4: File path on TTS")
    

    return  tts_path, json_path, stt_path
"""
