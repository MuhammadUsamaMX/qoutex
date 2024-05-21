import asyncio
import re
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import dotenv_values
import signal
import sys
import os
from main import *

# Load environment variables
env_vars = dotenv_values('.env')
# Time Differance
differance_in_time=6
#Duration of trade
duration=5

# Function to extract signal data from message text
def extract_signal_data(text):
    # Regular expression pattern to extract signal data
    pattern = r"Currency Pair: ([^\n]+)|Start Time: ([^\n]+)|📍 Position: ([^\n]+)"
    matches = re.findall(pattern, text)
    if matches:
        signal_data = {}
        for match in matches:
            if match[0]:  # Currency Pair
                signal_data["Currency Pair"] = match[0].replace("/", "").strip()
            elif match[1]:  # Start Time
                signal_data["Time"] = int(match[1].split(":")[1])  # Extract minutes and convert to integer
            elif match[2]:  # Position
                position = match[2].strip().upper()
                signal_data["Position"] = "put" if "DOWN" in position else "call"
        return signal_data
    else:
        return None

async def trade(signal_data):
    check_connect, message = await connect()
    while True:
        current_time = datetime.now()
        remaining_seconds = (signal_data["Time"] - current_time.minute - 1) * 60 + (60 - current_time.second)
        remaining_seconds=remaining_seconds-differance_in_time
        if remaining_seconds <= 8 or remaining_seconds <= 24 or remaining_seconds <= 32 or remaining_seconds <= 48 or remaining_seconds <= 56: 
            
            if not check_connect:
                check_connect, message = await connect()
                print("Trying to Authenticate For tarde ")

        if remaining_seconds <= 0:  # Also start before 2 seconds
            break
        print(f"Remaining seconds: {remaining_seconds}\r")
        await asyncio.sleep(1)
    try:
        await buy_and_check_win_3(1,signal_data["Currency Pair"]+"_otc", signal_data["Position"],duration)
    except Exception as e:
        print("While executing trade, Error occurred:", e)

async def main():
    # Set up Telegram client
    client = TelegramClient('session_name', int(env_vars['API_ID']), env_vars['API_HASH'])

    # Connect to Telegram API
    await client.start()

    # Define the Telegram entity (channel, group, etc.) ID
    entity_id = -1002009134814  # Replace with your channel ID AMIR VIP SIGNALS (1001945788775)

    # Event handler for new messages
    @client.on(events.NewMessage(chats=entity_id))
    async def handler(event):
        if "Signal" in event.message.message:
            await trade(extract_signal_data(event.message.message))

    print("Listening for new messages...")
    await client.run_until_disconnected()

asyncio.run(main())