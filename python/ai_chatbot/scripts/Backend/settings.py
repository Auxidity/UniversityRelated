"""
File : settings.py
Author : Daniel Kortesmaa
Description : Functions to set configs, and return them to main to be stored inside variables.
"""

#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""
import caller
import subprocess

def info_language():
    info_str = (
        "\nPossible languages to choose from: \n"
        "1. English\n"
        "2. French\n"
    )
    return info_str


def language(lang_var):
   
    while True: 
        if lang_var == "1":
            lang_tts = "English"
            lang_stt = "en-US"
            break
        elif lang_var == "2":
            lang_tts = "French"
            lang_stt = "fr-FR"
            break
        else:
            print(info_language())

    return lang_tts, lang_stt

def ip():
    ip = input("Enter IP for NaoQI: \n")
    return ip



"""
Cheatsheet for the led groups : http://doc.aldebaran.com/2-5/naoqi/sensors/alleds.html
Color list for naoqi leds:  (supported colors: “white”, “red”, “green”, “blue”, “yellow”, “magenta”, “cyan”).
"""
def info_color():
    color_info_str = (
        "1 = White\n"
        "2 = Red\n"
        "3 = Green\n"
        "4 = Blue\n"
        "5 = Yellow\n"
        "6 = Magenta\n"
        "7 = Cyan"
        )
    return color_info_str

def color(color_var):
    while True:
        if color_var == "1":
            out = "1" #White
            break
        elif color_var == "2":
            out = "2" #Red
            break
        elif color_var == "3":
            out = "3" #Green
            break
        if color_var == "4":
            out = "4" #Blue
            break
        elif color_var == "5":
            out = "5" #Yellow
            break
        elif color_var == "6":
            out = "6" #Magenta
            break
        elif color_var == "7":
            out = "7" #Cyan
            break
        else:
            print(info_color())
    return out

def change_led(ip, color):
    _, _, _, led_path =  caller.get_f_path()
    #Color is default that can be changed inside main.

    #Set eyes to specified color color.
    out = subprocess.Popen(['python2', led_path, ip, color], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_real, error = out.communicate()
    if out_real is not None:
        out_real_real = out_real.strip()
        print(out_real_real)
    else:
        print("Error in changing led", error)
    return 0

