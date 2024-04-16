import asyncio
import aiomysql
from telethon import TelegramClient, events
from dotenv import dotenv_values
import requests

# Load environment variables
env_vars = dotenv_values('.env')
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + env_vars['Google_API_KEY']  # Google API key
headers = {"Content-Type": "application/json"}

async def process_new_message(message):
    # Convert the message to lower case before checking for "time zone"
    if 'time zone' in message.lower():
        print("True")
        
        data = {"contents": [{"parts": [{"text": "Give me start time (minitus like 00,10,15,25,20),asset (currency pair in ######_otc fomat eg USKPKR_otc ) and direction (higher,up and other synonyms as call and lower,down,put as put )  Give me json key value pair like asset,direction,time ." + message}]}]}
        # Make the API request
        response = requests.post(api_url, headers=headers, json=data)
        # Parse the JSON response and extract the text value
        response_data = response.json()
        if 'candidates' in response_data and len(response_data['candidates']) > 0 and 'content' in response_data['candidates'][0]:
            content_parts = response_data['candidates'][0]['content']['parts']
            text_value = ' '.join([part['text'] for part in content_parts])

        print(text_value)



async def main():
    # Set up Telegram client
    client = TelegramClient('session_name', int(env_vars['API_ID']), env_vars['API_HASH'])

    # Connect to Telegram API
    await client.start()

    # Define the Telegram entity (channel, group, etc.) to listen to
    entity = await client.get_entity(-1001945788775)  # Replace with your channel ID

    # Listen for new messages in the channel and process them
    @client.on(events.NewMessage(chats=entity))
    async def handler(event):
        await process_new_message(event.message.text)

    print(f"Listening for new messages in channel: {entity.title}")
    await client.run_until_disconnected()

# Run the asynchronous function
asyncio.run(main())
