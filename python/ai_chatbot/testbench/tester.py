"""
File : tester.py
Author : Daniel Kortesmaa
Description :  Testbench. Add more test cases as I come up with neccesities. It is kind of ass since server needs to be threaded
"""

#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import unittest #Testbench dependancy
from unittest.mock import patch, MagicMock #To simulate tts subprocesses. GOD BLESS.
import subprocess
import time
import threading #To run server in parallel. Testbench is making it really inefficient.

import sys #Potentially neccesary?
import os
import queue

#Test
# Add the parent directory to sys.path so Python can find the modules in the 'scripts' directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(parent_dir, 'scripts'))



import file_reader
import chatbot_text
import gui_skeleton





def test_chatbot_function(): #Chatbot_Text. Outside server.
        # Define mock user input
    user_input = ["1","Hello", "exit"]

        # Patch input function to simulate user input
    with patch('builtins.input', side_effect=user_input):
          chatbot_text.main()  


def launch_server():
    try:
        server_process = subprocess.Popen(['python3', '/home/auxi/Desktop/AI/ai_chatbot/scripts/main.py'], stderr=subprocess.PIPE)
        server_process.wait()
    except subprocess.CalledProcessError as e:
        print("Process failed:",e)
        return False
    return True
        

def shutdown_server():
    try:
        cli_process = subprocess.Popen(['python3', '/home/auxi/Desktop/AI/ai_chatbot/scripts/gui_skeleton.py'], stdin=subprocess.PIPE)
        cli_process.communicate(input=b'0\n')
    except subprocess.CalledProcessError as e:
        print("GUI process failed:", e)
        return False
    return True

def file_transmission():
    try:
        cli_process = subprocess.Popen(['python3', '/home/auxi/Desktop/AI/ai_chatbot/scripts/gui_skeleton.py'], stdin=subprocess.PIPE)
        cli_process.communicate(input=b'1\nexit\n')

        
    except subprocess.CalledProcessError as e:
        print("GUI process failed:", e)
        return False
    finally:
        cli_process.terminate()
    return True


task_queue = queue.Queue()

task_queue.put(file_transmission)
task_queue.put(shutdown_server)


# Create threads for running the server, GUI, and tests
server_thread = threading.Thread(target=launch_server)
server_thread.start()

#Wait for server to start?
server_thread.join(timeout=1)

if server_thread.is_alive():
    print("Server didn't start within the timeout period.")
    # Handle the case where the server didn't start within the timeout period
    # You might want to abort the test or take other appropriate action
else:
    print("Server started successfully.")

# Execute tasks sequentially
while not task_queue.empty():
    task = task_queue.get()
    result = task()
    if not result:
        print("Task failed:", task.__name__)
        break

# Wait for all threads to finish
server_thread.join()

if not result:
    print("Some of the tasks failed.")
else:
    print("All tasks finished successfully.")