"""
File : main.py
Author : Daniel Kortesmaa
Description : main executable responsible for calling submodules and giving them neccesary arguments for succesful run
"""
import caller
import file_reader
import chatbot_text
import chatbot_speech
import sys
import settings


def info():
    info_str = (
        "Version : 0.3.4\n"
        "Input 0 if you wish to exit\n"
        "Input 1 if you wish to access file reading\n"
        "Input 2 if you wish to access single question mode\n"
        "Input 3 if you wish to access text based question mode with memory\n"
        "Input 4 if you wish to access speech based question mode with memory\n"
        "Input 5 if you wish to reconfigure\n"
        "Input 6 if you wish to add a configuration\n"
        "Input 7 if you wish to remove a configuration\n"
        "8 for debug\n"
        "DISCLAIMER: Not everything is implemented, unimplemented features return back to prompting for desired feature. Some implementations might not work as desired."
    )
    return info_str


def load():
    try:
        result1, result2, result3 = caller.get_f_path()
        #print(result1, result2, result3) #Debug
        return 0
    except caller.FilePathError as e:
        print(f"{e}")
        return 4

def ip_config():
    ip = settings.ip()
    return ip

def execute():
    print(settings.info_language())
    lang_tts, lang_stt = settings.language()
    ip = ip_config()
    print(info())
    while True:
        print("")
        command = input("Input: ")

        if command == "0":
            sys.exit()

        elif command == "1":
            file_reader.main(ip, lang_tts)
            
        elif command == "2":
            loader = load()
            if loader == 4:
                print("Exiting.")
                break
            else:
                caller.main(ip, lang_tts, lang_stt)


        elif command == "3":
            loader = load()
            if loader == 4:
                print("Exiting.")
                break
            else:
                chatbot_text.main()

        elif command == "4":
            loader = load()
            if loader == 4:
                print("Exiting.")
                break
            else:
                chatbot_speech.main(ip, lang_stt, lang_tts)

        elif command == "5":
            ip = ip_config()
            print(settings.info_language())
            lang_tts, lang_stt = settings.language()

        
        elif command == "6":
            _,json_path,_ = caller.get_f_path()
            caller.append_config(json_path, caller.create_entry())
        
        elif command == "7":
            _, json_path, _ = caller.get_f_path()
            caller.remove_entry(json_path,input("ID to remove: "))
        
        elif command == "8":
            load()

        else:
            print("\n")
            print(info())

if __name__ == "__main__":
    execute()