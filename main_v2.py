import os
import re
import sys
import json
import math
import random
import asyncio
import logging
from datetime import datetime
import pyfiglet
import configparser
from pathlib import Path
from dotenv import dotenv_values
from quotexapi.stable_api import Quotex
from telethon import TelegramClient, events

def resource_path(relative_path: str | Path) -> Path:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_dir = Path(__file__).parent
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_dir = Path(sys._MEIPASS)
    return base_dir / relative_path


config_path = Path(os.path.join(".", "settings/config.ini"))
if not config_path.exists():
    config_path.parent.mkdir(exist_ok=True, parents=True)
    text_settings = (f"[settings]\n"
                     f"email={input('Enter account email: ')}\n"
                     f"password={input('Enter account password: ')}\n"
                     f"email_pass={input('Enter email account password: ')}\n"
                     f"user_data_dir={input('Enter a path to the browser profile: ')}\n"
                     )
    config_path.write_text(text_settings)

config = configparser.ConfigParser()

config.read(config_path, encoding="utf-8")

email = config.get("settings", "email")
password = config.get("settings", "password")
email_pass = config.get("settings", "email_pass")
user_data_dir = config.get("settings", "user_data_dir")

if not email.strip() or not password.strip():
    print("Email and Password cannot be blank...")
    sys.exit()
if user_data_dir.strip():
    user_data_dir = "browser/instance/quotex.default"

client = Quotex(email=email,
                password=password,
                email_pass=email_pass,
                user_data_dir=Path(os.path.join(".", user_data_dir))
                )


# client.debug_ws_enable = True

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')


# PRACTICE mode is default / REAL mode is optional
# client.set_account_mode("REAL")


# Load environment variables
env_vars = dotenv_values('.env')

def asset_parse(asset):
    new_asset = asset[:3] + "/" + asset[3:]
    if "_otc" in asset:
        asset = new_asset.replace("_otc", " (OTC)")
    else:
        asset = new_asset
    return asset

async def connect(attempts=3):
    check, reason = await client.connect()
    if not check:
        attempt = 0
        while attempt <= attempts:
            if not client.check_connect():
                check, reason = await client.connect()
                if check:
                    print("Reconnected successfully!!!")
                    break
                else:
                    print("Error reconnecting.")
                    attempt += 1
                    if Path(os.path.join(".", "session.json")).is_file():
                        Path(os.path.join(".", "session.json")).unlink()
                    print(f"Trying to reconnect, attempt {attempt} from {attempts}")
            elif not check:
                attempt += 1
            else:
                break
            await asyncio.sleep(2)
        return check, reason
    print(reason)
    return check, reason

async def get_balance():
    check_connect, message = await connect()
    if check_connect:
        print("Current balance: ", await client.get_balance())
    print("Leaving...")
    client.close()

async def wait_until_start(time):
    pass
    
async def trading(time, amount_percentage = 1,asset = "USD/EGP_otc", direction = "put", duration = 5):  # in seconds
    
    check_connect, message = await connect()
    current_balance=  await client.get_balance()
    amount=current_balance*(amount_percentage)/100 
    
    while True:
        current_time = datetime.now()
        remaining_seconds = (time - current_time.minute - 1) * 60 + (60 - current_time.second)
        if (remaining_seconds < 30) and (remaining_seconds > 5):
            await connect()
        print(f"\rTarde start in {remaining_seconds} seconds ", end="")
        await asyncio.sleep(1)

        if remaining_seconds <= 2:  # Also start before 2 seconds

            try:             
                status, buy_info = await client.buy(amount, asset, direction, duration)
                print(status, buy_info)
                if await client.check_win(buy_info["id"]):
                    print(f"\nWin!!! \nWe beat kids!!!\nProfit:R$ {client.get_profit()}")
                else:
                    print(f"\nLoss    !!! \nMake New Trade with 2x amount the amount")
                    status, buy_info = await client.buy(amount*2, asset, direction, duration)
                    print(status, buy_info)
                    if await client.check_win(buy_info["id"]):
                        print(f"\nWin!!! \nWe beat kids!!!\nProfit:R$ {client.get_profit()}")
                    else:
                        print(f"\nLoss!!! \nMake New Trade with 4x amount the amount")
                        check_connect, message = await connect()
                        status, buy_info = await client.buy(amount*4, asset, direction, duration)
                        print(status, buy_info)
                        if await client.check_win(buy_info["id"]):
                            print(f"\nWin!!! \nWe beat kids!!!\nProfit:R$ {client.get_profit()}")
                        else:
                            print(f"\n Loss: R$ {client.get_profit()}")
            except: 
                print("Operation failed!!!")
            client.close()
            break

async def assets_open():
    check_connect, message = await connect()
    if check_connect:
        print("Check Asset Open")
        for i in client.get_all_asset_name():
            # print(i)
            print(i, client.check_asset_open(i))
    print("Leaving...")
    client.close()

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

async def websocket_manager():
    while True:
        if hasattr(client, "websocket_client") and client.websocket_client is not None and not client.websocket_client.is_connected:
            print("WebSocket is not connected. Reconnecting...")
            await connect()
        await asyncio.sleep(60)  # Check every minute

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
            try:
                tp = await trading(signal_data["Time"], asset=signal_data["Currency Pair"]+"_otc", direction=signal_data["Position"],duration = 5)
            #     if(tp == False):
            #         await trading(signal_data["Time"]+300, asset=signal_data["Currency Pair"]+"_otc", direction=signal_data["Position"],duration = 300)
            # #       return True
            except Exception as e:
                print("While executing trade, Error occurred:", e)
    print("Listening for new messages...")
    await asyncio.gather(websocket_manager(), client.run_until_disconnected())

# Call the main function within an asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
