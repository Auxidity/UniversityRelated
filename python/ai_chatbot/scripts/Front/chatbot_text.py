"""
File : chatbot_text.py
Author : Daniel Kortesmaa
Description : Text based chatbot with memory that can be configured based on configs available in config.json
"""
#Copyright disclaimer
"""
This project incorporates publicly accessible libraries and materials. The use of these libraries and materials is permitted under their respective licenses. However, any original content created by any author is not under any right to be used, reproduced, modified, distributed, or exploited. This prohibition applies to source code, documentation, and any derived work from this project. This prohibition does not apply to educational, research or reporting purposes.
For clarity, this means that only the publicly accessible libraries and materials can be used freely under their respective licenses. If you wish to use any original content created by author, you must obtain permission from author in question in writing.
"""

import api_call_memory


def main(config):
    
    chatgpt_config = config
    
    if chatgpt_config is not None:

        conversation_history = [
            {"role": "system", "content": chatgpt_config}
        ]

        log_path = "log_text.txt"
        with open(log_path, 'w') as log:
             pass

        while True:
            current_input = input("\nType exit to stop chatting. Message: ") #Payload message
            
            #Exit out
            if current_input.lower() == 'exit':
                break


            conversation_history.append({"role": "user", "content": current_input})

            #Api call
            response = api_call_memory.openai_api_call(conversation_history)

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
