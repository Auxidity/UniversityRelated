"""
File     : fsm.py
Author   : Daniel Kortesmaa
Desc.    : Magic. Hopefully. Trying to create a FSM back-end that publishes mqtt messages for gui (controlling the gui). Utilizes the other files for functions.
"""

#IPC signal to handle nested thread for SR
SR_MIC_BROADCAST_KILLSWITCH = "src/thread_alive.txt"
#IPC signal to handle speech_module thread lifespan
SR_THREAD_KILLSWITCH = "src/killswitch.txt"

import threading
import paho.mqtt.client as mqtt
import time, os, sys, signal, json, asyncio

#Telegram specific
from telethon.sync import TelegramClient

#Personal file imports. Who knows how we'll refactor these.
import mqtt_broker
import mqtt_sub
import reddit_api
import speech_module
import telegram_api
#import flask_auth SOMETHING IS WRONG WITH THIS. creates endless amounts of session files (when it shouldnt)

MQTT_BROKER = "localhost"  # Update with your MQTT broker details
MQTT_TOPIC = "tmp/topic"  # Update with your MQTT topic

class ExitSignal(Exception):
    pass

class StateMachine:
    def __init__(self):
        self.buffer = [] #To store mqtt messages
        self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.current_state = StateInitial(self.mqtt_client)

    def on_message(self, client, userdata, message):
        message_text = message.payload.decode()
        if message_text != '':
            self.buffer.append(message_text) #Maybe unneccesary
            print(message_text)
            self.current_state.handle_message(message_text)

            #Testing state switch as mqtt event
            next_state = self.current_state.run_pre_transition()
            if next_state != self.current_state:
                next_state.predecessor = self.current_state
                self.current_state = next_state
            #print(f"{self.current_state}    {next_state}    {self.current_state.predecessor}")

    def run(self):
        self.connect_mqtt()
        self.current_state.run_pre_transition()

        try:
            self.mqtt_client.loop_forever()
        finally:
            self.disconnect_mqtt()

    def connect_mqtt(self):
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(MQTT_BROKER, 1883)
        self.mqtt_client.subscribe(MQTT_TOPIC)

    def disconnect_mqtt(self):
        if self.mqtt_client:
            self.mqtt_client.disconnect()
            self.mqtt_client = None

class State:
    def __init__(self, mqtt_client, buffer = None, predecessor = None):
        if buffer is None:
            self.buffer = []
        else:
            self.buffer = buffer

        self.mqtt_client = mqtt_client
        self.cached_buffer = None
        self.predecessor = predecessor

    def run_pre_transition(self):
        pass

    def handle_transition(self):
        pass

    def clear_buffer(self):
        if self.buffer is not None:
            self.buffer = []
        else:
            self.buffer = []
    
    def cache_buffer(self):
        self.cached_buffer = self.buffer

    def clear_cache(self):
        self.cached_buffer = None

    def handle_message(self, message):
        words = message.split()
        self.buffer.extend(words)

    def pause_listening(self):
        if os.path.exists(SR_MIC_BROADCAST_KILLSWITCH):
            os.remove(SR_MIC_BROADCAST_KILLSWITCH)

    def start_listening(self):
        if not os.path.exists(SR_MIC_BROADCAST_KILLSWITCH): 
            open(SR_MIC_BROADCAST_KILLSWITCH, "w").close()

    def return_to_predecessor(self):
        if self.predecessor:
            return self.predecessor
        else:
            print("No predecessor state committed to memory")
            return self

class StateInitial(State):
    def __init__(self, mqtt_client, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)

        print("Switched to Initial")
        #self.clear_buffer()
        
    @staticmethod
    def kill_command():
        raise ExitSignal

    def run_pre_transition(self):
        #This is handled here for same reason we do it in the the state switcher state, although here it should work without the check under normal conditions. But just in case somethign dumb happens on runtime, 
        #we will get the IPC signal "high" periodically. as it should stay "high" the entire time (=logical 1 for the thread to do stuff)
        self.start_listening()

        print(self.buffer)

        return self.handle_transition(self.buffer)
    
    def handle_transition(self, buffer):
        for word in buffer:
            if word == "reddit":
                print("Moving to reddit")
                return StateReddit(self.mqtt_client, predecessor=self)
            elif word == "telegram":
                print("Moving to telegram")
                return StateTelegram(self.mqtt_client, predecessor=self)
            elif word == 'exit' or word == 'quit':
                self.kill_command()
        else:
            return self

class StateReddit(State):
    def __init__(self, mqtt_client, buffer=None, predecessor=None, keywords = None, subreddits = None):
        super().__init__(mqtt_client, buffer, predecessor)
        print("Switched to Reddit")
        self.mqtt_client.publish(MQTT_TOPIC, "Reddit state entered")
        self.clear_buffer()

        self.keywords = keywords
        self.subreddits = subreddits

        #Debugging if we can see if we can in fact go to predecessor state and add keywords etc.
        print(f"{self.keywords}, {self.subreddits}")

    def run_pre_transition(self):
        self.pause_listening()
        self.remove_stateswitch_message_from_buffer()
        return self.handle_transition()
    
    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["Reddit", "state", "entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    def fetch_a_post(self, keywords, subreddit_name):
        num_posts = 15
        out = reddit_api.output(keywords, subreddit_name, num_posts)
        for formatted_post in out:
            print(formatted_post, end='')

    def handle_transition(self):
        if self.keywords == None:
            print(self.keywords)
            print(self.subreddits)
            return StateKeywords(self.mqtt_client, predecessor=self)
        
        elif self.keywords != None and self.subreddits == None:
            print("While technically this would be really nice if we could bounce around between states while maintaining memory inside the object, when we go for second loop, we somehow end up not going back to this object.")
            #Well, we do go to the same object in same memory location, but for some reason the __init__ is ran again, and we lose the temporary knowledge that would be stored inside self.keywords or self.subreddits.
            #So we actually instead of coming back to this state with half finished stateReddit with either self.keywords or self.subreddits knowledge to run fetch_a_post(), its better to create a pipeline after which we can for sure run
            #fetch_a_post(). If we wish to add further functionality, we could iterate over buffer for different functions instead of only this one fetch a post like in stateInitial. Afterall, we don't store fetch_a_post critical data
            #in buffer,  only initially (inside the fetcher states) fetch it from buffer.
            return self
        
        elif self.keywords != None and self.subreddits != None:
            self.fetch_a_post(self.keywords, self.subreddits)
            return StateSwitchToInitial(self.mqtt_client, predecessor=self)
    
        else:
            print(self.keywords)
            print(self.subreddits)
            return self
"""
Ideally I wouldn't have made these as separate states, however due to functionality being extremely brittle, doing intermediary state switches where we pass arguments procedurally turned out to be the easiest solution that is still 
purely interrupt handled while functioning. Any while loop either turns out to be endless when its not meant to be one, or CPU useage spikes to 100% and stays there while also often leading to deadlocks anyway. Current solution remains
with low CPU useage.
"""
class StateKeywords(State):
    def __init__(self,mqtt_client, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        print("Switched to the state in which we fetch keywords")
        self.mqtt_client.publish(MQTT_TOPIC, "fetcher_entered")
        self.clear_buffer()
        self.prev_length = 0

    def run_pre_transition(self):
        self.start_listening()
        self.remove_stateswitch_message_from_buffer()
        return self.handle_transition()
    
    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["fetcher_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]
    
    def handle_transition(self):
        if self.prev_length == 0:
            print("Please submit your keywords to use for a search. After submitting keywords, say no to continue, clear to empty the current search terms or yes to continue adding keywords.")
        if len(self.buffer) != self.prev_length:
            self.prev_length = len(self.buffer)

            if self.buffer[-1] == "no":
                self.buffer.remove("no")                
                print(self.buffer)
                if len(self.buffer) == 0:
                    print("No keywords detected. Please try again")
                    self.prev_length = 0
                    return self
                else:
                    print(f"Keywords selected: {self.buffer}")
                    return StateSubredditKeywords(self.mqtt_client, keywords=self.buffer, predecessor=self)
            
            elif self.buffer[-1] == "yes":
                self.buffer.remove("yes")
                self.prev_length -= 1
                print(self.buffer)
                return self
            
            elif self.buffer[-1] == "clear":
                self.buffer = []
                print("Buffer cleared!")
                self.prev_length = 0
                return self
            
            else:
                print("Do you wish to submit more keywords? No to continue, clear to empty current search, yes to continue adding keywords")
                return self
        else:
            return self
    

class StateSubredditKeywords(State):
    def __init__(self,mqtt_client, keywords, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.keywords = keywords
        print("Switched to the state in which we fetch subreddits")
        self.mqtt_client.publish(MQTT_TOPIC, "subreddit_fetcher_entered")
        self.prev_length = 0

    def run_pre_transition(self):
        self.start_listening()
        self.remove_stateswitch_message_from_buffer()
        return self.handle_transition()

    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["subreddit_fetcher_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]    
    
    def handle_transition(self):
        if len(self.buffer) == 0:
            print("Please enter which subreddits you would like to search from? Say no to perform the search, yes to add more subreddits or clear to clear the buffer.")

        if len(self.buffer) != self.prev_length:
            self.prev_length = len(self.buffer)

            if self.buffer[-1] == "no":
                self.buffer.remove("no")
                if len(self.buffer) == 0:
                    print("Nothing has been entered!")
                    self.prev_length = 0
                    return self
                else:
                    print(f"Searching using: {self.keywords}, from: {self.buffer}")
                    return StateReddit(self.mqtt_client, buffer = None, predecessor=self, keywords=self.keywords, subreddits=self.buffer)
            
            elif self.buffer[-1] == "yes":
                self.buffer.remove("yes")
                self.prev_length -= 1
                return self
            
            elif self.buffer[-1] == "clear":
                self.buffer = []
                print("Buffer cleared!")
                self.prev_length = 0
                return self
            
            else:
                print("Do you wish to submit more subreddits? Say no to perform the search, yes to add more subreddits or clear to clear the buffer.")
                return self
        else:
            return self          

class StateTelegram(State):
    def __init__(self, mqtt_client, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        print("Switched to Telegram")
        self.mqtt_client.publish(MQTT_TOPIC, "Telegram_state_entered")
        self.clear_buffer()

    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["Telegram_state_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    def run_pre_transition(self):
        self.remove_stateswitch_message_from_buffer()
        return self.handle_transition()
    
    def handle_transition(self): #We dont reach here anymore. 
        return StateTelegramAuthInit(self.mqtt_client, predecessor=self)

class StateTelegramAuthInit(State):
    def __init__(self, mqtt_client, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.mqtt_client.publish(MQTT_TOPIC, "Telegram_auth_entered")
    
    def run_pre_transition(self):
        if self.authentication_successful():
            self.mqtt_client.publish(MQTT_TOPIC, "Auth_succesful")
            return StateTelegramMain(self.mqtt_client, predecessor=self)
        
        else:
            print("Auth not succesful")
            return StateTelegramAuthPhone(self.mqtt_client, predecessor=self)
        
    def create_client_instance(self):
        #Load API credentials for Telegram API
        try:
            with open('src/telegram.json') as f:
                config = json.load(f)
                api_id = config['api_id']
                api_hash = config['api_hash']
                redirect_url = config['redirect_url']
        except FileNotFoundError as e:
            print(f"Pathing issue on finding api credentials due to hardcoded path. Full error: \n{e}")
            sys.exit(2)

        session_name = telegram_api.load_name()

        #Instanced telegram client
        client = TelegramClient(session_name, api_id, api_hash)
        return client

    def authentication_successful(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        out = asyncio.run(telegram_api.prev_session_exists(self.create_client_instance()))
        print(out)
        return out

        
class StateTelegramAuthPhone(State):
    def __init__(self, mqtt_client, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.buffer = []
        self.mqtt_client.publish(MQTT_TOPIC, "Telegram_phone_authentication_entered")
        self.country_code = None
        self.phone_number = None

    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["Telegram_phone_authentication_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    def run_pre_transition(self):
        self.remove_stateswitch_message_from_buffer()
        return self.handle_transition()
    
    def handle_transition(self):
        if len(self.buffer) == 0 and self.country_code == None:
            print("Enter your country code (e.g. +358)")
        print(self.buffer)

        if len(self.buffer) > 0 and self.country_code == None:
            print("Would you like to confirm the current as input for country code?")
            print("If you wish to do so, say yes. Otherwise keep saying numbers until the displayed message fits the country code.")
            if self.buffer[-1] == "yes":
                self.buffer.remove("yes")
                self.country_code = ''.join(self.buffer)

                if telegram_api.validate_country_code(self.country_code) is True:
                    print("Please enter phone number now")
                    self.buffer = []
                    return self
                else:
                    self.buffer = []
                    self.country_code = None

        elif len(self.buffer) > 0 and self.country_code != None:
            print("Would you like to confirm the current as input for phone number? If not, keep inputting numbers")
            print("Correct format for phone number is having 10 numbers in it, in local format (so the first number is always 0). E.g. 045 123 4567")
            if self.buffer[-1] == "yes":
                self.buffer.remove("yes")
                self.phone_number = ''.join(self.buffer)

                if telegram_api.validate_input_local_number(self.phone_number) is True:
                    valid_number = self.country_code + self.phone_number
                    print(f"Valid number: {valid_number}")
                    return StateTelegramCodeAuth(self.mqtt_client, predecessor=self, phone=valid_number)
                else:
                    print("Invalid number")
                    self.buffer = []
                    self.phone_number = None

        return self
    
class StateTelegramCodeAuth(State):
    def __init__(self, mqtt_client, phone, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.telegram_client = None
        self.phone = phone
        self.mqtt_client.publish(MQTT_TOPIC, "Telegram code authentication state entered")


    def create_client_instance(self):
        #Load API credentials for Telegram API
        try:
            with open('src/telegram.json') as f:
                config = json.load(f)
                api_id = config['api_id']
                api_hash = config['api_hash']
                redirect_url = config['redirect_url']
        except FileNotFoundError as e:
            print(f"Pathing issue on finding api credentials due to hardcoded path. Full error: \n{e}")
            sys.exit(2)

        session_name = telegram_api.load_name()

        #Instanced telegram client
        client = TelegramClient(session_name, api_id, api_hash)
        return client

    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["Telegram", "code", "authentication", "state", "entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]
        

    def run_pre_transition(self):
        self.remove_stateswitch_message_from_buffer()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.telegram_client = self.create_client_instance()
        asyncio.run(telegram_api.fsm_auth(self.telegram_client, self.phone))

        return self.handle_transition()
    
    def handle_transition(self):
        return StateTelegramAuthInit(self.mqtt_client, predecessor=self)

class StateTelegramMain(State):
    def __init__(self, mqtt_client, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.mqtt_client.publish(MQTT_TOPIC, "Telegram_main_state_entered")

    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["Telegram_main_state_entered", "Auth_succesful"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    async def async_user_data_fetch(self):
        telegram_client = self.create_client_instance()
        await telegram_client.start()
        await telegram_api.fetch_contacts(telegram_client) #Is used to initialize a contacts json that then is used locally instead of making repeated api calls
        await telegram_client.disconnect()

    def create_client_instance(self):
        #Load API credentials for Telegram API
        try:
            with open('src/telegram.json') as f:
                config = json.load(f)
                api_id = config['api_id']
                api_hash = config['api_hash']
                redirect_url = config['redirect_url']
        except FileNotFoundError as e:
            print(f"Pathing issue on finding api credentials due to hardcoded path. Full error: \n{e}")
            sys.exit(2)

        session_name = telegram_api.load_name()

        #Instanced telegram client
        client = TelegramClient(session_name, api_id, api_hash)
        return client
    
    def check_user_data_exists(self):
        if not os.path.exists('user_data.json'):
            time.sleep(1)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            asyncio.run(self.async_user_data_fetch()) #Is used to initialize a contacts json that then is used locally instead of making repeated api calls
        else:
            pass

    def run_pre_transition(self):
        self.start_listening()
        self.remove_stateswitch_message_from_buffer()
        self.check_user_data_exists()
        return self.handle_transition()

    def handle_transition(self):
        print("We are in main functionality. Say 'help' if you wish to see all possible functions")
        print(self.buffer)
        for word in self.buffer:
            if word == "quit":    
                return StateSwitchToInitial(self.mqtt_client, predecessor=self)

            elif word == "history":
                self.buffer = [] #So we dont endless loop ourselves here when returning
                return StateTelegramSearch(self.mqtt_client, predecessor=self, route="history")

            elif word == "message":
                self.buffer = []
                return StateTelegramSearch(self.mqtt_client, predecessor=self, route="message")

            elif word == "search":
                self.buffer = []
                return StateTelegramSearch(self.mqtt_client, predecessor=self, route="search")
                
            elif word == "help":
                print("This is a helpful message. Possible actions include 'search', 'message' and 'history'.")
                self.buffer.remove("help")
                self.buffer = []
            
            else:
                print("Speak help outloud to view all possible commands")
                self.buffer = []

        return self

    
class StateTelegramHistory(State):
    def __init__(self, mqtt_client, search_id, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.mqtt_client.publish(MQTT_TOPIC, "Telegram_history_state_entered")
        self.search_id = search_id

    def create_client_instance(self):
        #Load API credentials for Telegram API
        try:
            with open('src/telegram.json') as f:
                config = json.load(f)
                api_id = config['api_id']
                api_hash = config['api_hash']
                redirect_url = config['redirect_url']
        except FileNotFoundError as e:
            print(f"Pathing issue on finding api credentials due to hardcoded path. Full error: \n{e}")
            sys.exit(2)

        session_name = telegram_api.load_name()

        #Instanced telegram client
        client = TelegramClient(session_name, api_id, api_hash)
        return client

    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["Telegram_history_state_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    async def asynchronous_task(self):
        telegram_client = self.create_client_instance()
        await telegram_client.start()
        await telegram_api.fetch_message_history(self.search_id, telegram_client)
        await telegram_client.disconnect()

    def run_pre_transition(self):
        self.remove_stateswitch_message_from_buffer()
        self.start_listening()
        return self.handle_transition()
    
    def handle_transition(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.asynchronous_task())
        return StateTelegramMain(self.mqtt_client, predecessor=self)
    


class StateTelegramMessage(State):
    def __init__(self, mqtt_client, target_id, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.mqtt_client.publish(MQTT_TOPIC, "Telegram_message_state_entered")
        self.target_id = target_id
        self.prev_length = 0

    def create_client_instance(self):
        #Load API credentials for Telegram API
        try:
            with open('src/telegram.json') as f:
                config = json.load(f)
                api_id = config['api_id']
                api_hash = config['api_hash']
                redirect_url = config['redirect_url']
        except FileNotFoundError as e:
            print(f"Pathing issue on finding api credentials due to hardcoded path. Full error: \n{e}")
            sys.exit(2)

        session_name = telegram_api.load_name()

        #Instanced telegram client
        client = TelegramClient(session_name, api_id, api_hash)
        return client

    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["Telegram_message_state_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    def run_pre_transition(self):
        self.remove_stateswitch_message_from_buffer()
        self.start_listening()
        return self.handle_transition()
    
    async def run_asynchronous_task(self, message):
        telegram_client = self.create_client_instance()
        await telegram_client.start()
        await telegram_api.send_message(self.target_id, message, telegram_client)
        await telegram_client.disconnect()
    
    def handle_transition(self):
        if self.prev_length == 0:
            print("Please speak out your message. Do not end your message in words 'send' or 'clear', as they are used to control the program here. As long as the sentences do not end in either of those two words, useage of them is fine.")
        
        if len(self.buffer) != self.prev_length:
            self.prev_length = len(self.buffer)
            print(self.buffer)

            if len(self.buffer) != 0 and self.buffer[-1] != "send" and self.buffer[-1] != "clear":
                print("If you wish to confirm the following as your message to be sent, please say 'send'")
                str_buf = " ".join(self.buffer)
                print("Otherwise, to start your message from scractch, say 'clear'. If you've decided against sending a message, end your sentence in 'quit'")
                print(f"Current message: {str_buf}")
            if self.buffer[-1] == "send":
                self.buffer.remove("send")
                str_buf = " ".join(self.buffer)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                asyncio.run(self.run_asynchronous_task(str_buf))
                return StateTelegramMain(self.mqtt_client, predecessor=self)
            elif self.buffer[-1] == "clear":
                self.buffer = []
                print(self.buffer)
            
            elif self.buffer[-1] == "quit":
                return StateTelegramMain(self.mqtt_client, predecessor=self)

        return self
    

class StateTelegramSearch(State):
    def __init__(self, mqtt_client, route, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.mqtt_client.publish(MQTT_TOPIC, "Telegram_search_state_entered")
        self.prev_length = 0
        self.route = route

    def remove_stateswitch_message_from_buffer(self):
        #God bledd initializing an empty buffer matters :)
        elements_to_remove = ["Telegram_search_state_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    def run_pre_transition(self):
        self.remove_stateswitch_message_from_buffer()
        self.start_listening()
        return self.handle_transition()
    
    def create_client_instance(self):
        #Load API credentials for Telegram API
        try:
            with open('src/telegram.json') as f:
                config = json.load(f)
                api_id = config['api_id']
                api_hash = config['api_hash']
                redirect_url = config['redirect_url']
        except FileNotFoundError as e:
            print(f"Pathing issue on finding api credentials due to hardcoded path. Full error: \n{e}")
            sys.exit(2)

        session_name = telegram_api.load_name()

        #Instanced telegram client
        client = TelegramClient(session_name, api_id, api_hash)
        return client  
      
    def handle_transition(self):
        if self.prev_length == 0:
            print("Please input who to search for")
        
        if len(self.buffer) != self.prev_length:
            self.prev_length = len(self.buffer)

            print(f"Would you like to search using {self.buffer}? If not, say no to clear search field.")
            
            if self.buffer[-1] == "yes" and self.route == "search":
                self.buffer.remove("yes")
                print(self.buffer)
                return StateTelegramSearchSub1(self.mqtt_client, search_target = self.buffer, predecessor = self, route = "search")
            
            elif self.buffer[-1] == "yes" and self.route == "history":
                self.buffer.remove("yes")
                print(self.buffer)
                return StateTelegramSearchSub1(self.mqtt_client, search_target = self.buffer, predecessor = self, route = "history")
            
            elif self.buffer[-1] == "yes" and self.route == "message":
                self.buffer.remove("yes")
                print(self.buffer)
                return StateTelegramSearchSub1(self.mqtt_client, search_target = self.buffer, predecessor = self, route = "message")
            
            elif self.buffer[-1] == "no":
                self.buffer = []
                print(self.buffer)
                self.prev_length = 0


        return self

class StateTelegramSearchSub1(State):
    def __init__(self, mqtt_client, search_target, route, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.search_target = search_target
        self.route = route
        self.mqtt_client.publish(MQTT_TOPIC, "TelegramSearchSubstate1_entered")
        self.data = None

    def remove_stateswitch_message_from_buffer(self):
        elements_to_remove = ["TelegramSearchSubstate1_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    def run_pre_transition(self):
        self.remove_stateswitch_message_from_buffer()
        return self.handle_transition()
    
    def fetch_users_from_userdata(self):
        data = telegram_api.load_usercontacts()
        search_target_string = "".join(self.search_target)
        self.data = telegram_api.search_contacts(data, search_target_string)
        print("search_contacts")
        return telegram_api.filter_search_fsm(self.data)
    
    def handle_transition(self):
        out = self.fetch_users_from_userdata()
        print(out, type(out))

        if out == 0: #Only 1 match
            id = telegram_api.get_fsm_matched_contact(self.data, "1")
            #print(id) Debug line. We "print" anyway. Other functions are then going to use this flow (and we add a predecessor chain logic to ensure we move to correct state later)
            if self.route == "search":
                return StateTelegramMain(self.mqtt_client, predecessor=self)
            elif self.route == "history":
                return StateTelegramHistory(self.mqtt_client, search_id=id, predecessor=self)
            elif self.route == "message":
                return StateTelegramMessage(self.mqtt_client, target_id=id, predecessor=self)
        
        elif out == 1: #Multiple matches
            return StateTelegramSearchSub2(self.mqtt_client, possible_matches = self.data, route=self.route, predecessor = self)
        
        elif out == 2: #No matches
            return StateTelegramMain(self.mqtt_client, predecessor=self)
        
        else:
            print("Shouldn't be possible to get here.")
            return self

class StateTelegramSearchSub2(State):
    def __init__(self, mqtt_client, possible_matches, route, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.possible_matches = possible_matches
        self.route = route
        self.mqtt_client.publish(MQTT_TOPIC, "TelegramSearchSubstate2_entered")
        self.prev_length = 0

    def remove_stateswitch_message_from_buffer(self):
        elements_to_remove = ["TelegramSearchSubstate2_entered"]
        self.buffer = [element for element in self.buffer if element not in elements_to_remove]

    def run_pre_transition(self):
        self.remove_stateswitch_message_from_buffer()
        return self.handle_transition()
    
    def handle_transition(self):
        if self.prev_length == 0:
            print("Select which enumerator represents the person you had in mind.")

        if len(self.buffer) != self.prev_length:
            self.prev_length = len(self.buffer)

            print(f"Would you like to confirm {self.buffer} as the enumerator? If not, say no to clear selection. Otherwise, say yes")
            if self.buffer[-1] == "yes":
                self.buffer.remove("yes")
                buffer_to_string = "".join(self.buffer)
                id = telegram_api.get_fsm_matched_contact(self.possible_matches, buffer_to_string)
                if self.route == "search":
                    print(id)
                    return StateTelegramMain(self.mqtt_client, predecessor=self)
                elif self.route == "history":
                    return StateTelegramHistory(self.mqtt_client, search_id=id, predecessor=self)
                elif self.route == "message":
                    return StateTelegramMessage(self.mqtt_client, target_id=id, predecessor=self)
            
            elif self.buffer[-1] == "no":
                self.buffer = []
                self.prev_length = 0

        return self

class StateSwitchToInitial(State):
    def __init__(self, mqtt_client, buffer=None, predecessor=None):
        super().__init__(mqtt_client, buffer, predecessor)
        self.clear_buffer() #We need to clear the buffer to avoid immediate transition, store the buffer potentially to cache and pass cache around
        print("reached init")
        self.mqtt_client.publish(MQTT_TOPIC, "SwitchToInitial state entered")

    def run_pre_transition(self):
        #This IPC needs to be handled here, if we return to an old object (this state) and we only do this in init, we won't launch speech service again resulting in a deadlock
        self.start_listening()


        print("reached check_transition")
        print(self.buffer)
        return self.handle_transition(self.buffer)
    
    def handle_transition(self, buffer):
        print("Do we reach here?")
        if buffer:
            for word in buffer:
                if word == "yes":
                    print("Moving to initial state")
                    self.cache_buffer()
                    self.clear_buffer()
                    return StateInitial(self.mqtt_client, predecessor=self)
                
                elif word == "no" and self.predecessor is not None:
                    print("Returning to predecessor")
                    self.clear_buffer()
                    return self.predecessor.__class__(self.mqtt_client, buffer=self.cached_buffer, predecessor=self)
                
                elif word == "no" and self.predecessor is None:
                    print("What the fuck did you just do? Nice deadlock")
                    return self

            else:
                print("We are essentially deadlocked here until you say yes :)")
                return self
        else:
            return self #Something wack happened to be here but o well



def signal_handler(sig, frame):
    # Handle the keyboard interrupt signal
    print("\nKeyboard interrupt detected. Exiting...")
    open(SR_THREAD_KILLSWITCH, 'w').close() #Kills the speech_thread, cleanup inside thread finally block
    sys.exit()

if __name__ == "__main__":
    try:
        # Set up the signal handler for SIGINT (KeyboardInterrupt). Killswitch
        signal.signal(signal.SIGINT, signal_handler)

        #Initialize speech recognition thread separately
        speech_thread = threading.Thread(target=speech_module.main)
        speech_thread.start()


        #Instance the FSM
        fsm = StateMachine()

        #Execute
        fsm.run()
    except ExitSignal:
        open(SR_THREAD_KILLSWITCH, 'w').close() #Kills the speech_thread, cleanup inside thread finally block 
        print("Exiting from inside FSM...")
        sys.exit()
    
    finally:
        fsm.disconnect_mqtt()

