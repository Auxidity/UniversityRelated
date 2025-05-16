"""
File     : flask_auth.py
Author   : Daniel Kortesmaa
Desc.    : Authentication service. Currently for reddit. Add telegram once I get API key working (which I got timeouted for so another day it is). Store credentials VERY SECURELY ":D" for now.
Potentially need to move all server side stuff under here..

More To Do's : instead of per session auth, do cookies or something(?) for longer term auth.
"""

"""
Flow for reddit auth (needs to be implemented in GUI, but if you skip a step shit won't work):

IMPORTANT!!!! ONLY HTTP. HTTPS won't work

connect to http://localhost:5000/auth
get redirect to callback_auth (if succesful)
connect to http://localhost:5000/make_api_call IN SAME SESSION!

Make it more robust later.
"""


from flask import Flask, request, redirect, session, url_for
import praw     #Reddit
import secrets  #Reddit
import requests #Telegram
import json     #Variable loading for API
from telethon.sync import TelegramClient
import uuid
import asyncio

from praw.models import Redditor #Debug, remove from live

"""
Token handler
"""
def generate_unique_token(length=16):  
    #Generate a unique token. change length as neccesary
    return secrets.token_urlsafe(length)

def store_unique_token(token):
    #Save the token into file. Change this approach into a db write, where it gets encrypted yada yada. Change loader once implemented
    with open('token.txt', 'w') as file:
        file.write(token)

def load_unique_token(filename='token.txt'):
    try:
        with open(filename, 'r') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        print(f"Token file didn't exist. Creating a new one.")
        token = generate_unique_token()
        store_unique_token(token)
        return token


app = Flask(__name__)
app.secret_key = load_unique_token()
app.telegram_access_token = None

#Load API credentials for Reddit API
with open('src/reddit.json') as f:
    config = json.load(f)
    user_agent_variable = config['user_agent']
    client_secret_variable = config['client_secret']
    client_id_variable = config['client_id']

reddit = praw.Reddit(
    client_id=client_id_variable,
    client_secret=client_secret_variable,
    redirect_uri='http://localhost:5000/auth_callback',
    user_agent= user_agent_variable 
)

#Load API credentials for Telegram API
with open('src/telegram.json') as f:
    config = json.load(f)
    api_id = config['api_id']
    api_hash = config['api_hash']
    redirect_url = config['redirect_url']

#Telegram client instance
session_name = str(uuid.uuid4())
client = TelegramClient(session_name, api_id, api_hash)

"""
Reddit authentication initialization. Change unique_key to a per session generated one later. Can use the generate_unique_key() for it.
"""
@app.route('/')
def index():
    return 'The very lively index.'

@app.route('/reddit_auth')
def reddit_auth():
    auth_url = reddit.auth.url(['identity', 'submit'], 'unique_key', 'permanent')
    return redirect(auth_url)

"""
Callback on reddit authentication
"""
@app.route('/reddit_auth_callback')
def reddit_auth_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state != 'unique_key':  # Validate state
        return 'Error: State mismatch'
    try:
        refresh_token = reddit.auth.authorize(code)
        session['refresh_token'] = refresh_token  # Store refresh token securely
        return 'Authentication successful! You can now make API calls.'
    except Exception as e:
        return f'Error: {str(e)}'

"""
Telegram auth
"""


#Note, everything is under test.py for now until something ACTUALLY works.

#TLDR: Dont use web server auth flow for telegram. 
#Session handling can be done through a .session file that is generated.
#Authentication works relatively well with a terminal input, which can be handled as a gui event but
#is problematic as a web server solution due to making a terminal call to web server and effectively deadlocking the server





"""
Api_call function. Currently returns the name of the user. 

To Do testing :

Create a private subreddit for testing commenting and creating posts and add their functionality.

Handle in the GUI with these api calls.
"""
@app.route('/make_api_call')
def make_api_call(): #Rename to whatever function we'll test first.
    refresh_token = session.get('refresh_token')
    if not refresh_token:
        return 'Error: User not authenticated'

    try:
        user = reddit.user.me()
        print(type(user))
        if isinstance(user, Redditor):
            print("Object is an instance of redditor class")
        
        else:
            print("Object is not an instance of redditor class")
        #return f'{refresh_token}'
        return f'{user.name}'

    except Exception as e:
        return f'Error: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True)

