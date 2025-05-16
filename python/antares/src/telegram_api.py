"""
File     : telegram_api.py
Author   : Daniel Kortesmaa
Desc.    : telegram authentication and app functionality all in one. Wanted to make authentication part of telegram in the 
flask auth file, but it isn't worth the hassle. Would need to somehow be able to inject commands to server terminal,
which in of itself sounds like a REALLY GREAT idea. The auth flow is different between reddit and telegram, so we split 
them apart for now. Due to this, dropping reddit comment & post functionality might make a lot of sense.
"""
import json, sys, os, secrets, asyncio 
import paho.mqtt.client as mqtt
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.types import InputPeerUser, InputPeerChat
from concurrent.futures import ThreadPoolExecutor

MAX_INPUT_LENGTH = 10 #To avoid potential overflows. The value is low, but who has 9999999999 duplicate entries? Only used in the while loop to avoid potential excess memory consumption. Apply to the search term aswell and
#change the max len to 100?

MQTT_BROKER = "localhost"  # Update with your MQTT broker details
MQTT_TOPIC = "tmp/topic"  # Update with your MQTT topic

current_dir = os.getcwd()
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

tokentxt_path = os.path.join(parent_dir, 'token.txt')

#Create session name using same token as reddit auth. Is used to hold for subsequent logins to bypass code verification every time. Change this later to be more secure (should be a 2 for 1 solution)
def generate_unique_token(length=16):  
    #Generate a unique token. change length as neccesary
    return secrets.token_urlsafe(length)

def store_unique_token(token):
    #Save the token into file. Change this approach into a db write, where it gets encrypted yada yada. Change loader once implemented
    with open('token.txt', 'w') as file:
        file.write(token)

def load_name(filename='token.txt'):
    try:
        with open(filename, 'r') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        print(f"Token file didn't exist. Creating a new one.")
        token = generate_unique_token()
        store_unique_token(token)
        return token
    
def get_phone():
    while True:
        country_code = input("Input country code (+358 in Finland): ")
        if validate_country_code(country_code):
            break
        else:
            print("Invalid country code. Please try again.")

    while True:
        local_number = input("Input phone number without country code: ")
        if validate_input_local_number(local_number):
            break
        else:
            print("Invalid phone number. Please try again.")
    return country_code + local_number

def validate_input_local_number(phone_number):
    # Remove all spaces from the input
    phone_number = phone_number.replace(" ", "")

    # Check if the first character is '0' and if the length of the input is 10 characters & doesnt contain anything but numbers
    if phone_number.startswith('0') and len(phone_number) == 10 and phone_number.isdigit():
        return True
    else:
        return False

def validate_country_code(country_code):
    valid_country_codes = ['+358']
    if country_code in valid_country_codes:
        print("Country code found")
        return True
    else:
        print("This country code is either not valid or not supported")
        return False

async def get_code():
    code = input("Input code. THIS IS NOT THE DEFAULT CALLBACK!: ")
    return code

#Authentication function. Might need something fancier? It does work though.
async def authenticate(phone_number = None):
    if phone_number is not None:
        try:
            # Start the client and authenticate
            await client.start(phone=phone_number, code_callback=get_code)
            print("Successfully authenticated!")
        except Exception as e:
            print(f"Error {e}")
    else:
        try:
            # Start the client and authenticate
            await client.start(code_callback=get_code)
            print("Successfully authenticated!")
        except Exception as e:
            print(f"Error {e}")

async def fsm_auth(client, phone_number):
    try:
        await client.connect()
        await client.start(phone=phone_number, code_callback=code_callback)
        print("Succesfully authenticated")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()


def code_callback():
    print("Reached callback function outside fsm. Please enter the code, and after entering it say yes. If you make a mistake, say clear to start again.")
    def on_message(client, userdata, message):
        global code
        message_text = message.payload.decode()
        if message_text != '':
            buffer.append(message_text) 
            print(buffer)
            if buffer[-1] == "yes":
                buffer.remove("yes")
                code = ''.join(buffer)
                client.disconnect()  # Disconnect client when "yes" is received
            elif buffer[-1] == "clear":
                buffer.clear()
                print(buffer)
    
    global buffer
    global code
    buffer = []
    code = None
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883)
    client.subscribe(MQTT_TOPIC)

    print("Starting loop")
    client.loop_forever()

    # This part is reached only after client.disconnect() is called
    client.disconnect()  # Ensure client disconnects after the loop
    print("Exiting loop")
    print(f"{code}, {type(code)}, {buffer}")
    return code

#Contact fetcher. Mostly magic to me.
async def fetch_contacts(client):
    #Fetch user info
    me = await client.get_me()

    #Get contacts dict. Raw thing is a mess.
    contacts = await client(GetContactsRequest(0))
    all_user_details = [] #Array to store users that have first name, last name or username field populated.

    for contact in contacts.contacts:
        # Accessing the user object associated with the contact
        user = await client.get_entity(contact.user_id)
        # Check if the contact has either first_name, last_name, or username populated
        if user.first_name or user.last_name or user.username:
            all_user_details.append(
                {"id": user.id, "first_name": user.first_name, "last_name": user.last_name,
                 "username": user.username, "phone": user.phone, "is_bot": user.bot}) #Trim down on the data stored when we figure out which parts of this we actually need for basic operations.

    with open('user_data.json', 'w') as outfile: #Debug file.
        json.dump(all_user_details, outfile)


def search_contacts(data, search_term):
    search_results =[]
    found_ids = set()

    for entry in data:
        #Search for either first_name, last_name or username. Handle none fields with and operator, where search_term.lower is always true but entry might not have first_name, last_name or username.
        if (entry['first_name'] and search_term.lower() in entry['first_name'].lower() or
            entry['last_name'] and search_term.lower() in entry['last_name'].lower() or
            entry['username'] and search_term.lower() in entry['username'].lower()):

            if entry['id'] not in found_ids:
                search_results.append(entry)
                found_ids.add(entry['id'])
    
    return search_results

def load_usercontacts():
    try:
        with open('user_data.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError as e:
        return f"Error: {e}"
    
def filter_search_fsm(data):
    if data:
        # If only one entry is found, print its first name and last name
        if len(data) == 1:
            entry = data[0]
            print(f"First Name: {entry['first_name']}, Last Name: {entry['last_name']}")
            return 0
        
        # Enumerate found results for easier identification
        else:
            print("Found results:")
            for i, entry in enumerate(data, start=1):
                print(f"{i}. First Name: {entry['first_name']}, Last Name: {entry['last_name']}")
            return 1
    else:
        print("No matching contacts found.")
        return 2

def get_fsm_matched_contact(data, selected_index):
    if not data:
        return None
    
    try:
        selected_index = int(selected_index)
        if 1 <= selected_index <= len(data):
            return data[selected_index - 1]['id']
        else:
            # Catches out of bounds
            print("Invalid input")
            return None
    except ValueError:
        # Catches invalid input
        print("Not an integer input")
        return None



#CLI ONLY
def filter_search_contacts(data):
    if data:
        # If only one entry is found, print its first name and last name
        if len(data) == 1:
            entry = data[0]
            print(f"First Name: {entry['first_name']}, Last Name: {entry['last_name']}")
            return entry['id']
        
        # Enumerate found results for easier identification
        print("Found results:")
        for i, entry in enumerate(data, start=1):
            print(f"{i}. First Name: {entry['first_name']}, Last Name: {entry['last_name']}")
        
        while True:
            try:
                # Return the chosen entry based on above enumeration
                selected_index = input("Enter the number corresponding to the entry you wish to select: ")
                if len(selected_index) > MAX_INPUT_LENGTH:
                    print("Input is too long. What are you trying to do?")
                else:
                    selected_index = int(selected_index)
                    if 1 <= selected_index <= len(data):
                        print(f"First Name: {data[selected_index - 1]['first_name']}, Last Name: {data[selected_index - 1]['last_name']}")
                        return data[selected_index - 1]['id']
                    else:
                        # Catches out of bounds
                        print("Invalid selection. Please enter a valid integer index.")
            except ValueError:
                # Catches everything else. Floats, mixed input (2Ha2hA), char
                print("Invalid input. Please enter an integer number.")
    else:
        return None

    
async def fetch_user_hash(user_id, client):
    #This function is a helper to create an instance of InputPeerUser
    try:
        user_entity = await client.get_entity(int(user_id))
        access_hash = user_entity.access_hash
        #print(type(access_hash)) debugger
        return access_hash
    except ValueError:
        return f"Invalid user ID"

async def fetch_message_history(user_id, client):
    user_hash = await fetch_user_hash(user_id, client)
    if user_hash:
        user = InputPeerUser(user_id, user_hash)

        messages = await client.get_messages(user, limit=10)
        for message in reversed(messages):
            print(message.text)

async def send_message(user_id, message, client):
    try:
        await client.send_message(int(user_id), message)
        print(f"Message {message} sent!")
    except ValueError:
        print("Invalid user ID.")

async def prev_session_exists(client):
    await client.connect()
    try:
        return await client.is_user_authorized()
    finally:
        await client.disconnect()



#Main file. Run this as a thread with inputs and commands from the mqtt pub ran through fsm
#For now just stand alone terminal. Hijack this to GUI later.
async def main(phone_number = None):
    if phone_number is not None:
        await authenticate(phone_number)
    else:
        await authenticate()

    try:
        await fetch_contacts()

        while True:
            command = input("Enter a command (fetch, search, messages, send, quit): ").lower()
            if command == 'fetch':
                await fetch_contacts()

            elif command == 'search':
                data = load_usercontacts()
                print('What to search with?')
                search_term = input()
                results = search_contacts(data, search_term)
                result = filter_search_contacts(results)
                print(result) #Change to return user_id

            elif command == 'messages':
                data = load_usercontacts()
                print("Whose messages do you wish to see? Enter name")
                search_term = input()
                results = search_contacts(data, search_term)
                result = filter_search_contacts(results)
                await (fetch_message_history(int(result)))

            elif command == 'send':
                data = load_usercontacts()
                print("To whom you wish to send a message? Enter name")
                search_term = input()
                results = search_contacts(data, search_term)
                result = filter_search_contacts(results)
                print("What message do you wish to send?")
                message = input()
                
                await send_message(result, message)

            elif command == 'quit':
                break

            else:
                print("Invalid command. Please enter 'fetch', 'search', 'messages' or 'quit'.")
                
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected, exiting!")
        sys.exit()

if __name__ == "__main__":
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

    session_name = load_name()

    #Instanced telegram client
    client = TelegramClient(session_name, api_id, api_hash)

    #client.sign_in()

    def run_main():
        asyncio.run(main(phone))

    #flag = prev_session_exists()
    if prev_session_exists() is True:
        phone = None
        run_main()
    
    else:
        phone = get_phone()
        run_main()
