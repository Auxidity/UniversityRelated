"""
File : chatbot_speech.py
Author : Daniel Kortesmaa
Description : Speech based chatbot with memory that can be configured based on configs available in config.json
"""
#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import caller
import api_call_memory
import subprocess
from stt import recognize_speech


def main(ip, stt_lang, tts_lang, chatgpt_config):

    ip_inside_main = ip
    tts_path, _, _, _ = caller.get_f_path()

    
    
    if chatgpt_config is not None:

        conversation_history = [
            {"role": "system", "content": chatgpt_config}
        ]

        log_path = "log_speech.txt"
        with open(log_path, 'w') as log:
             pass

        while True:
            current_input = recognize_speech(stt_lang)
            #print(current_out, errors, stt_out) #Debug

            #print("\n") #To show what you said in terminal, comment out if undesired
            #print(current_input) #This is done inside recognize_speech currently.
            #Exit out on timeout
            if current_input == 2:
                print("Timeout reached")
                break


            conversation_history.append({"role": "user", "content": current_input})

            #Api call
            response = api_call_memory.openai_api_call(conversation_history)

            #TTS call.
            subprocess.Popen(['python2', tts_path, response, ip_inside_main, tts_lang], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            

            #Display result & append it to payload
            print("\n")
            print(response)
            conversation_history.append({"role": "assistant", "content": response})

            # Write to log file
            with open(log_path, 'a') as log:
                log.write(f"User: {current_input}\nResponse: {response}\n\n")


    else:
         return 3 #Error code 3, somehow skipped def config()
        


if __name__ == "__main__":
    main()