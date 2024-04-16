import asyncio
import json
from telethon import TelegramClient, events
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values('.env')

# Function to prepare message data for JSON serialization
def prepare_message_for_json(message):
    return {
        "id": message.id,
        "sender_id": message.sender_id,
        "date": message.date.strftime('%Y-%m-%d %H:%M:%S'),
        "text": message.message
    }

async def main():
    # Set up Telegram client
    client = TelegramClient('session_name', int(env_vars['API_ID']), env_vars['API_HASH'])

    # Connect to Telegram API
    await client.start()

    # Define the Telegram entity (channel, group, etc.) ID
    entity_id = -1001945788775  # Replace with your channel ID

    # Path where to save the JSON file
    file_path = 'all_messages.json'

    # Ensure the JSON file exists and is empty or contains a valid JSON array
    with open(file_path, 'a+') as f:
        f.seek(0)
        if not f.read(1):  # File is empty
            f.write('[]')  # Initialize file with an empty JSON array

    # Event handler for new messages
    @client.on(events.NewMessage(chats=entity_id))
    async def handler(event):
        # Prepare message data for JSON
        message_data = prepare_message_for_json(event.message)
        
        # Append the new message data to the JSON file
        with open(file_path, 'r+') as f:
            # Read the current data
            f.seek(0)
            data = json.load(f)
            # Append the new message
            data.append(message_data)
            # Write the updated data back to the file
            f.seek(0)
            f.truncate()  # Clear the file before re-writing
            json.dump(data, f, ensure_ascii=False, indent=4)

    print("Listening for new messages...")
    await client.run_until_disconnected()

# Run the asynchronous function
asyncio.run(main())
