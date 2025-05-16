#!/usr/bin/python2
"""
File : leds.py
Author : Daniel Kortesmaa
Description : file to change robot eye colors to indicate states of speaking and listening.
"""

#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

from naoqi import ALProxy
import sys


def set_eye_color(ip, color):
    print(color) #Debug

    if color == '1':
        out = 0x00FFFFFF #White
        
    elif color == '2':
        out = 0x00FF0000 #Red
        
    elif color == '3':
        out = 0x0000FF00 #Green
        
    if color == '4':
        out = 0x000000FF #Blue
        
    elif color == '5':
        out = 0x00FFFF00 #Yellow
        
    elif color == '6':
        out = 0x00FF00FF #Magenta
        
    elif color == '7':
        out = 0x0000FFFF #Cyan
    
    else:
        out = 0x00000000 #Errors as black
        
    eye_colors = ALProxy("ALLeds", ip, 9559)

    
    eye_colors.fadeRGB("FaceLeds", out, 1)
    #eye_colors.listGroup("FaceLeds")
    

    return 0

if __name__ == "__main__":
    # Check if all arguments is provided
    if len(sys.argv) < 3:
        print("Usage: python ")
        sys.exit(1)

    #Give ip to the function
    ip = sys.argv[1]

    color= sys.argv[2]

    # Call the function to perform text-to-speech
    set_eye_color(ip, color)
    









