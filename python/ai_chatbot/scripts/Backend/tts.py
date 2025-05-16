#!/usr/bin/python2
"""
File : tts.py
Author : Daniel Kortesmaa
Description : tts module to naoqi robot.
"""

#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

from naoqi import ALProxy
import sys

"""
Two modes of speech, hardcode whichever is preferred. Rest are deprecated.  
ALAnimatedSpeechProxy  --random animations while speaking
ALTextToSpeech  --loudspeaker
"""

def text_to_speech(text, ip, lang):
    tts = ALProxy("ALTextToSpeech", ip, 9559)
    tts.setLanguage(lang)
    tts.say(text)
    return 0

if __name__ == "__main__":
    # Check if all arguments is provided
    if len(sys.argv) < 4:
        print("Usage: python tts.py <text_to_speak> <ip> <lang>")
        sys.exit(1)

    # Get the text to be spoken from the command line argument
    text_to_speak = sys.argv[1]
    
    #Give ip to the function
    ip = sys.argv[2]

    lang = sys.argv[3]

    # Call the function to perform text-to-speech
    text_to_speech(text_to_speak, ip, lang)
    









