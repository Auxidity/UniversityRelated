"""
File : stt.py
Author : Daniel Kortesmaa
Description : stt module of AI chatbot
"""
#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import os
import speech_recognition as sr
import time

TIMEOUT = 30

def recognize_speech(lang):
    # Save current file descriptors
    #save_stdout = os.dup(1)
    save_stderr = os.dup(2)

    # Redirect stdout and stderr to /dev/null or nul
    
    os.close(2)
    os.open(os.devnull, os.O_WRONLY)

    try:
        language=lang
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            pause_threshold = 0.5  # Set a threshold for pauses in speech (in seconds)
            audio = recognizer.listen(source, timeout=TIMEOUT)
            
            #data = recognizer.recognize_google_cloud(audio, credentials_json=None, language="en-US", preferred_phrases=None, show_all=False)

        try:
            text = recognizer.recognize_google(audio, language=language)
            print(text)
            return text
        
        except sr.UnknownValueError:
            pass
        
        
        except sr.RequestError as e:
            return 1 #Error code RequestError
        
        if recognizer.energy_threshold > pause_threshold:
                time.sleep(pause_threshold)
        return 2
        

    finally:
        # Restore stdout and stderr
        os.dup2(save_stderr, 2)
        os.close(save_stderr)

if __name__ == "__main__":

    recognize_speech(lang="en-US")
