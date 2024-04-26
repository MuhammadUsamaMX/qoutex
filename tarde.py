import asyncio
import re
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import dotenv_values
import signal
import sys
import os

# Load environment variables
env_vars = dotenv_values('.env')

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
    return None

async def wait_until_start(start_time):
    while True:
        remaining_seconds = (start_time - datetime.now().minute - 1) * 60 + (60 - datetime.now().second)
        if remaining_seconds <= 10:
            break
        print(f"Remaining seconds: {remaining_seconds - 10}\r")
        await asyncio.sleep(1)

async def trading(signal_data):
    await wait_until_start(signal_data["Time"])
    try:
        # Assuming buy_and_check_win_3 is defined elsewhere
        await buy_and_check_win_3(amount_percentage=1, asset=f"{signal_data['Currency Pair']}_otc", direction=signal_data["Position"], duration=300)
        print("Trade Run Successfully!")
    except Exception as e:
        print("While executing trade, Error occurred:", e)


def check_program_status():
    if os.path.exists('istarted.ini'):
        with open('istarted.ini', 'r') as file:
            status = file.read().strip()
            print(f"Program is {status}")
            if status == 'stopped':
                print("Program is stopped. Starting...")
                # Run the asynchronous function
                asyncio.run(main())
            else:
                print("Already running....")
    else:
        print("Program is not started yet.")

async def main():

    # Write "started" to the 'istarted.ini' file
    with open('istarted.ini', 'w') as file:
        file.write('started')

    # Set up Telegram client
    client = TelegramClient('session_name', int(env_vars['API_ID']), env_vars['API_HASH'])

    # Connect to Telegram API
    await client.start()

    # Define the Telegram entity (channel, group, etc.) ID
    entity_id = -1002009134814  # Replace with your channel ID AMIR VIP SIGNALS (1001945788775)

    # Event handler for new messages
    @client.on(events.NewMessage(chats=entity_id))
    async def handler(event):
        message_text = event.message.message.lower()  # Convert message to lowercase for case insensitivity
        if "signal" in message_text:
            signal_data = extract_signal_data(event.message.message)
            if signal_data:
                print(signal_data)
                await trading(signal_data)
        if "trading report" in message_text and "4th session" in message_text:
            print("Exiting program and stopping all processes...")
            await client.disconnect()
            sys.exit()

    print("Listening for new messages...")
    await client.run_until_disconnected()

    # Write "stopped" to the 'istarted.ini' file upon program exit
    with open('istarted.ini', 'w') as file:
        file.write('stopped')


def exit_handler(sig, frame):
    print("Forcefully terminating the program...")
    with open('istarted.ini', 'w') as file:
        file.write('stopped')
    sys.exit(0)

# Register the exit handler for SIGINT and SIGTERM signals
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# Start the check_program_status
check_program_status()
