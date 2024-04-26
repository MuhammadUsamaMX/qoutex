import asyncio
import re
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import dotenv_values
import signal
import sys
import os
from main import buy_and_check_win_3

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
    else:
        return None

async def wait_until_start(start_time):
    while True:
        current_time = datetime.now()
        remaining_seconds = (start_time - current_time.minute - 1) * 60 + (60 - current_time.second)
        if remaining_seconds <= 18:  # Also start before 18 seconds
            break
        print(f"Remaining seconds: {remaining_seconds-18}\r")
        await asyncio.sleep(1)

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
            signal_data = extract_signal_data(event.message.message)
            # print(signal_data)
            await wait_until_start(signal_data["Time"])
            try:
                await buy_and_check_win_3(amount_percentage=1, asset=signal_data["Currency Pair"]+"_otc", direction=signal_data["Position"],duration = 5)
        #       return True
            except Exception as e:
                print("While executing trade, Error occurred:", e)

            # Write "stopped" to the 'istarted.ini' file upon program exit
            with open('istarted.ini', 'w') as file:
                file.write('stopped')

            print("Exiting program and stopping all processes...")
            await client.disconnect()
            sys.exit()

    print("Listening for new messages...")
    await client.run_until_disconnected()


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
