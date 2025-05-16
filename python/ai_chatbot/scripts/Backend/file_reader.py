"""
File : file_reader.py
Author : Daniel Kortesmaa
Description : script for opening a file and then printing the entire content to terminal. Later on add tts.py with file as arg when tts.py functionality has been confirmed.
"""
#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import subprocess
import caller, settings



def main(ip, tts_lang, content, color):
    lang_tts = tts_lang
    ip_inside_main = ip
    text = content
    tts_path, _, _, led_path =  caller.get_f_path()
    #Color is default that can be changed inside main.

    #Set eyes to specified color color. Hardcoded for now
    subprocess.Popen(['python2', led_path, ip_inside_main, "red"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)



    #TTS call using content
    subprocess.Popen(['python2', tts_path, text, ip_inside_main, lang_tts], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    #Set eyes back to white (default)
    subprocess.Popen(['python2', led_path, ip_inside_main, color], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    
    
    return 0

if __name__ == "__main__":
    main()