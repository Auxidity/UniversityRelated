import telegram_api, os, sys, json, secrets, asyncio
from telethon.sync import TelegramClient

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

session_name = load_name()
try:
    with open('src/telegram.json') as f:
        config = json.load(f)
        api_id = config['api_id']
        api_hash = config['api_hash']
        redirect_url = config['redirect_url']
except FileNotFoundError as e:
    print(f"Pathing issue on finding api credentials due to hardcoded path. Full error: \n{e}")
    sys.exit(2)

client = TelegramClient(session_name, api_id, api_hash)

def create_client():
    client = TelegramClient(load_name(), api_id, api_hash)
    return client


print(asyncio.run(telegram_api.prev_session_exists(create_client())))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

asyncio.run(telegram_api.fsm_auth(create_client(),"+3580451376447"))

