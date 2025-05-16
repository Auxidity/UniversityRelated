"""
File : gui_skeleton.py
Author : Daniel Kortesmaa
Description : skeleton to communicate with main.py Build GUI on top of this functionality.
"""

#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import sys
import client_comm
import socket
import json
import chatbot_text


HOST = '127.0.0.1'
PORT = 1337


"""
Language codes for server:
1 = English
2 = French
"""


def info():
    info_str = (
        "Version : 0.5.7\n"
        "Input 0 if you wish to exit\n"
        "Input 1 if you wish to send file transmission\n"
        "Input 2 for chatbot_text\n"
        "Input 3 for having a speech based chat with chatbot\n"


        
        "\n4 for debug (inspect payload)\n"
        "Input 5 if you wish to reconfigure commands\n"
        "Input 6 if you wish to send the current payload as custom payload\n"
        "Input 7 for adding a new chatgpt configuration\n"
        "8 for debug single speech payload\n"
        "9 for debug change led variable single payload\n"
        "10 for debug change led single payload\n"
        "\nDISCLAIMER: Not everything is implemented, unimplemented features return back to prompting for desired feature. Some implementations might not work as desired."
    )
    return info_str

def info_sub():
    info_str = (
        "What to reconfigure? \n"
        "1 for command\n"
        "2 for ip\n"
        "3 for config_id\n"
        "4 for lang\n"
        "5 for content1\n"
        "6 for content2"
    )
    return info_str

def execute():
    print("Copyright (c) 2024, Daniel Kortesmaa\n"
    "All rights reserved.")

    print(info())
    server_command, ip, config_id, lang, content1, content2 = client_comm.construct_initial_payload_content()
    while True:
        print("")
        command = input("Main Input: ")

        
        if command == "0": #Kill command
            server_command, ip, config_id, lang, content1, content2 = client_comm.construct_server_kill()
            payload = client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(payload).encode())
            response = client_socket.recv(1024).decode()
            print(response)
            client_socket.close()
            sys.exit()

        elif command == "1": #File reading through tts
            server_command = "1"
            content1 = client_comm.file_as_string()
            if content1 != 1:
                #print(content1) #Debug
                payload = client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((HOST, PORT))
                client_socket.sendall(json.dumps(payload).encode())
                response = client_socket.recv(1024).decode()
                client_socket.close()
                print(response)
            else:
                print("No file selected!")



        elif command == "2": #Chatbot_text
            var = input("Id to use: ")
            var2 = "6"
            payload = client_comm.construct_payload(var2, ip, config_id, lang, var, content2)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(payload).encode())
            response = client_socket.recv(1024).decode()
            
            client_socket.close()
            if response != "No entry with given ID":
                chatbot_text.main(response)
            else:
                print(response)

        elif command == "3": #Chatbot_speech. 
            #Design choice to be made for prompt config to be default and set elsewhere or prompt before calling.
            server_command = "3"
            config_id = client_comm.config_id()
            payload = client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(payload).encode())
            response = client_socket.recv(1024).decode()
            
            print(response) #Hide later
            with open("client_log_speech.txt", "w") as file:
                file.write(response)

            client_socket.close()


        

        elif command == "4": #Print the payload
            payload = client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            print(payload)



        elif command == "5": #Change payload contents
            print(info_sub())
            sub_command = input("Sub Input: ")
            if sub_command == "1":
                server_command = client_comm.command()
                client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            elif  sub_command == "2":
                ip = client_comm.ip()
                client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            elif sub_command == "3":
                config_id = client_comm.config_id()
                client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            elif sub_command == "4":
                lang = client_comm.language()
                client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            elif sub_command == "5":
                content1 = client_comm.content()
                client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            elif sub_command == "6":
                content2 = client_comm.alt_content()
                client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            else:
                print(info_sub())

        elif command == "6": #Constructs a custom payload from current variables and sends it
            
            payload = client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            #print(payload) #Debug
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(payload).encode())
            response = client_socket.recv(1024).decode()
            print(response)
            client_socket.close()

        elif command == "7": #Add a new entry
            server_command = "4"
            content = input("Id to use: ")
            content2 = input("Description of the desired chatbot: ")

            payload = client_comm.construct_payload(server_command, ip, config_id, lang, content, content2)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(payload).encode())
            response = client_socket.recv(1024).decode()
            print(response)
            client_socket.close()


        elif command == "8": #Debug payload for a single transmission (stt, tts, leds)
            server_command = "2"
            ip = client_comm.ip()
            config_id = client_comm.config_id()
            lang = client_comm.language()

            payload = client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(payload).encode())
            response = client_socket.recv(1024).decode()
            client_socket.close()
        
        elif command == "exit": #Testbench command to shut down the gui but not server.
            sys.exit()

        elif command == "9": #Debug led switch config
            server_command = "7"
            ip = client_comm.ip()
            content1 = client_comm.content()

            payload = client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(payload).encode())
            response = client_socket.recv(1024).decode()
            print(response)
            client_socket.close()


        elif command == "10": #Debug call led switch command
            server_command = "8"
            payload = client_comm.construct_payload(server_command, ip, config_id, lang, content1, content2)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(payload).encode())
            response = client_socket.recv(1024).decode()
            print(response)
            client_socket.close()

        else:
            print(info())
            


if __name__ == "__main__":
    execute()