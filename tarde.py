import asyncio
import re
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import dotenv_values
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
                signal_data["Position"] = "PUT" if "DOWN" in position else "CALL"
        return signal_data
    else:
        return None

async def wait_until_start(start_time):
    while True:
        current_time = datetime.now()
        remaining_seconds = (start_time - current_time.minute - 1) * 60 + (60 - current_time.second)
        if remaining_seconds <= 18:  # Also start before 18 seconds
            break
        print(f"Remaining seconds: {remaining_seconds}")
        await asyncio.sleep(1)

async def trading(signal_data):
    await wait_until_start(signal_data["Time"])
    try:
        await buy_and_check_win_3(amount_percentage=1, asset=signal_data["Currency Pair"]+"_otc", direction=signal_data["Position"])
    except Exception as e:
        print("Error occurred while executing buy_and_check_win_3:", e)

async def main():
    # Set up Telegram client
    client = TelegramClient('session_name', int(env_vars['API_ID']), env_vars['API_HASH'])

    # Connect to Telegram API
    await client.start()

    # Define the Telegram entity (channel, group, etc.) ID
    entity_id = -1002009134814  # Replace with your channel ID

    # Event handler for new messages
    @client.on(events.NewMessage(chats=entity_id))
    async def handler(event):
        if "Signal" in event.message.message:
            signal_data = extract_signal_data(event.message.message)
            print(signal_data)
            await trading(signal_data)

    print("Listening for new messages...")
    await client.run_until_disconnected()

# Run the asynchronous function
asyncio.run(main())
