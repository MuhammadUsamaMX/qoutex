import asyncio
import socket
import json  # Import json for serialization
from telethon import TelegramClient, events
from dotenv import dotenv_values
import re

# Load environment variables
env_vars = dotenv_values('.env')

client = TelegramClient('session_name', int(env_vars['API_ID']), env_vars['API_HASH'])

# Define the Telegram entity (channel, group, etc.) ID
entity_id = -1002009134814  # Replace with your channel ID AMIR VIP SIGNALS (1001945788775)

# Setup socket for IPC
producer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
producer_socket.connect(('localhost', int(env_vars['PORT']))) # Connect to consumer script listening on port 9999

async def start_telegram_client():
     await client.start()
     if not await client.is_user_authorized():
         await client.send_code_request(phone)
         try:
             await client.sign_in(phone, input('Enter the verification code: '))
         except SessionPasswordNeededError:
             await client.sign_in(password=input('Password: '))


# Function to extract signal data from message text
def extract_signal_data(text):
    # Regular expression pattern to extract signal data
    pattern = r"Currency Pair: ([^\n]+)|Start Time: ([^\n]+)|📍 Position: ([^\n]+)"
    matches = re.findall(pattern, text)
    try:
        signal_data = {}
        for match in matches:
            if match[0]:  # Currency Pair
                signal_data["pair"] = match[0].replace("/", "").strip()
            elif match[1]:  # Start Time
                signal_data["time"] = int(match[1].split(":")[1])  # Extract minutes and convert to integer
            elif match[2]:  # Position
                position = match[2].strip().upper()
                signal_data["Position"] = "put" if "DOWN" in position else "call"
        return signal_data
    except Exception as e:
         print(f"Error parsing message: {e}")
    return None

# Event handler for new messages
@client.on(events.NewMessage(chats=entity_id))
async def handler(event):
    if "Signal" in event.message.message:
        signal = extract_signal_data(event.message.message)            
        if signal:
            # Convert the dictionary to a JSON string
            signal_json = json.dumps(signal)
            # Send this JSON string over the socket
            producer_socket.sendall(signal_json.encode('utf-8'))

async def main():
     await start_telegram_client()
     await client.run_until_disconnected()

if __name__ == "__main__":
     asyncio.run(main())