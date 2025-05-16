"""
File : main.py
Author : Daniel Kortesmaa
Description : localhost server that handles backend.
"""
#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import settings
import caller
import file_reader
import chatbot_speech
import socket
import json
import sys

HOST = '127.0.0.1'
PORT = 1337

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the port to be reused
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((HOST, PORT))
except OSError as e:
    if e.errno == 98:
        server_socket.close()
        server_socket.bind((HOST,PORT))
    else:
        raise

server_socket.listen(5)

print("Copyright (c) 2024, Daniel Kortesmaa\n"
    "All rights reserved.")

print("Version 0.5.7\n")

print("Sanity saver:\n"
      "0 to exit\n"
      "1 for file reader\n"
      "2 single question\n"
      "3 speech chatbot\n"
      "4 add config\n"
      "5 remove config\n"
      "6 for chatbot id fetch\n"
      "7 for custom led config (not used but functionality exists)"
      )

global default_led_color
default_led_color = "1"

while True:
    client_socket, addr = server_socket.accept()

    #Receive data
    data = client_socket.recv(1024).decode()

    #Parse the payload
    payload = json.loads(data)

    # Extract values from the payload
    command = payload["command"]
    ip = payload["ip"]
    config_id = payload["config_id"]
    lang = payload["lang"]
    content = payload["content"]
    content2 = payload["alt_content"]

    lang_tts, lang_stt = settings.language(lang)

    
    
    


    if command == "0":
        response = "Nuut nuut"
        client_socket.sendall(response.encode())
        server_socket.close()
        sys.exit()
    
    elif command == "1": #File reader
        #print(lang_tts, ip, content) #Debug
        file_reader.main(ip, lang_tts, content,default_led_color)
        print("Command 1 succesfully executed")
        response = "Nuut nuut"
        
    
    elif command == "2": #Single question, mostly debug status?
        error_code = caller.main(ip, lang_tts, lang_stt, config_id, default_led_color)
        if error_code == 0:
            response = "Nuut nuut"
            print("Command 2 succesfully executed")
        else:
            response = error_code              
    
    elif command == "3": #Speech chatbot
        chatbot_speech.main(ip, lang_stt, lang_tts, config_id)
        with open("log_speech.txt", "r") as file:
            response = file.read()
            if not response:
                response = "Nuut Nuut"


        print("Command 3 succesfully executed")
    
    elif command == "4": #Add chatbot config
        _, json_path, _, _ = caller.get_f_path()
        response = caller.append_config(json_path, caller.create_entry(content, content2))
        print("Command 4 succesfully executed")
        
    
    elif command == "5": #Remove chatbot config
        _, json_path, _, _ = caller.get_f_path()
        response = caller.remove_entry(json_path, content)
        print("Command 5 succesfully executed")
    
    elif command == "6": #ID fetcher
        _, json_path, _, _ = caller.get_f_path()
        response = caller.config_fetcher(json_path, content)
        if response is not None:
            print("Command 6 succesfully executed")
            pass
        else:
            response = "No entry with given ID"
    
    elif command == "7": #Change led color 
        default_led_color = settings.color(content)
        print(f"Led color set to {default_led_color}")
        response = f"You've set color variable to {default_led_color}"
    
    elif command == "8":
        print("Command received")
        print(default_led_color)
        settings.change_led(ip, content)
        response = "Nuut Nuut"
        
    
    else:
        response = "Invalid command"
    
    # Send response back to the client
    client_socket.sendall(response.encode())
    
