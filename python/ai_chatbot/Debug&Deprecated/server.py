"""
File : main.py
Author : Daniel Kortesmaa
Description : localhost server that handles backend.
"""
import settings
import caller
import file_reader
import chatbot_text
import chatbot_speech
import socket
import json
import sys

HOST = '127.0.0.1'
PORT = 691337

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(5)




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
    content2 = payload("content2")

    lang_tts, lang_stt = settings.language(lang)


    if command == "0":
        response = "Nuut nuut"
        client_socket.sendall(response.encode())
        server_socket.close()
        sys.exit()
    
    elif command == "1":
        file_reader.main(ip, lang_tts, content)
        response = "Nuut nuut"
        
    
    elif command == "2":
        error_code = caller.main(ip, lang_tts, lang_stt)
        if error_code == 0:
            response = "Nuut nuut"
        else:
            response = error_code
        
    
    elif command == "3": #Revisit this
        chatbot_text.main()
        response = "Nuut nuut"
        
    
    elif command == "4":
        chatbot_speech.main(ip, lang_stt, lang_tts, config_id)
        response = "Nuut nuut"
    
    elif command == "5":
        _, json_path, _ = caller.get_f_path()
        response = caller.append_config(json_path, caller.create_entry(content, content2))
        
    
    elif command == "6":
        _, json_path, _ = caller.get_f_path()
        response = caller.remove_entry(json_path, content)
        
    
    else:
        response = "Invalid command"
    
    # Send response back to the client
    client_socket.sendall(response.encode())
    
