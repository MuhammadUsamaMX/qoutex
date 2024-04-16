# import re
# import asyncio
# from datetime import datetime, timedelta
# import asyncio
# import aiomysql
# from telethon import TelegramClient, events
# from dotenv import dotenv_values
# import requests
# import os
# import sys
# import json
# import random
# import logging
# import pyfiglet
# import configparser
# from pathlib import Path
# from quotexapi.stable_api import Quotex


# def extract_signal_info(text):
#     # Define regular expressions to extract information
#     timezone_pattern = r"Time Zone:\s*(\S+)"
#     currency_pair_pattern = r"Currency Pair:\s*(\S+)"
#     start_time_pattern = r"Start Time:\s*(\d{2}:\d{2})"
#     position_pattern = r"Position:\s*\((\w+)\)"

#     # Extract information using regular expressions
#     timezone_match = re.search(timezone_pattern, text)
#     currency_pair_match = re.search(currency_pair_pattern, text)
#     start_time_match = re.search(start_time_pattern, text)
#     position_match = re.search(position_pattern, text)

#     # Check if all information is found
#     if timezone_match and currency_pair_match and start_time_match and position_match:
#         timezone = timezone_match.group(1)
#         currency_pair = currency_pair_match.group(1)
#         start_time = start_time_match.group(1)
#         position = position_match.group(1)
#         return {
#             "Time Zone": timezone,
#             "Currency Pair": currency_pair,
#             "Start Time": start_time,
#             "Position": position
#         }
#     else:
#         return None


# # __author__ = "Cleiton Leonel Creton"
# # __version__ = "1.0.0"

# # __message__ = f""
# # # Use in moderation, as management is everything!
# # # support: cleiton.leonel@gmail.com or +55 (27) 9 9577-2291
# # # """

# def resource_path(relative_path: str | Path) -> Path:
#     """Get absolute path to resource, works for dev and for PyInstaller"""
#     base_dir = Path(__file__).parent
#     if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
#         base_dir = Path(sys._MEIPASS)
#     return base_dir / relative_path


# config_path = Path(os.path.join(".", "settings/config.ini"))
# if not config_path.exists():
#     config_path.parent.mkdir(exist_ok=True, parents=True)
#     text_settings = (f"[settings]\n"
#                      f"email={input('Enter account email: ')}\n"
#                      f"password={input('Enter account password: ')}\n"
#                      f"email_pass={input('Enter email account password: ')}\n"
#                      f"user_data_dir={input('Enter a path to the browser profile: ')}\n"
#                      )
#     config_path.write_text(text_settings)

# config = configparser.ConfigParser()

# config.read(config_path, encoding="utf-8")

# custom_font = pyfiglet.Figlet(font="ansi_shadow")
# ascii_art = custom_font.renderText("PyQuotex")
# art_effect = "Demo"

# # print(art_effect)

# email = config.get("settings", "email")
# password = config.get("settings", "password")
# email_pass = config.get("settings", "email_pass")
# user_data_dir = config.get("settings", "user_data_dir")

# if not email.strip() or not password.strip():
#     print("Email and Password cannot be blank...")
#     sys.exit()
# if user_data_dir.strip():
#     user_data_dir = "browser/instance/quotex.default"

# client = Quotex(email=email,
#                 password=password,
#                 email_pass=email_pass,
#                 user_data_dir=Path(os.path.join(".", user_data_dir))
#                 )


# # client.debug_ws_enable = True

# # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')


# # PRACTICE mode is default / REAL mode is optional
# # client.set_account_mode("REAL")


# def asset_parse(asset):
#     new_asset = asset[:3] + "/" + asset[3:]
#     if "_otc" in asset:
#         asset = new_asset.replace("_otc", " (OTC)")
#     else:
#         asset = new_asset
#     return asset


# async def connect(attempts=5):
#     check, reason = await client.connect()
#     if not check:
#         attempt = 0
#         while attempt <= attempts:
#             if not client.check_connect():
#                 check, reason = await client.connect()
#                 if check:
#                     print("Reconnected successfully!!!")
#                     break
#                 else:
#                     print("Error reconnecting.")
#                     attempt += 1
#                     if Path(os.path.join(".", "session.json")).is_file():
#                         Path(os.path.join(".", "session.json")).unlink()
#                     print(f"Trying to reconnect, attempt {attempt} from {attempts}")
#             elif not check:
#                 attempt += 1
#             else:
#                 break
#             await asyncio.sleep(5)
#         return check, reason
#     print(reason)
#     return check, reason


# async def get_balance():
#     check_connect, message = await connect()
#     if check_connect:
#         print("Current balance: ", await client.get_balance())
#     print("Leaving...")
#     client.close()


# async def get_profile():
#     check_connect, message = await connect()
#     if check_connect:
#         profile = await client.get_profile()
#         description = (f"\nUser: {profile.nick_name}\n"
#                        f"Demo Balance: {profile.demo_balance}\n"
#                        f"Actual Balance: {profile.live_balance}\n"
#                        f"Id: {profile.profile_id}\n"
#                        f"Avatar: {profile.avatar}\n"
#                        f"Country: {profile.country_name}\n"
#                        )
#         print(description)
#     print("Leaving...")
#     client.close()


# # Load environment variables
# env_vars = dotenv_values('.env')
# api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + env_vars['Google_API_KEY']  # Google API key
# headers = {"Content-Type": "application/json"}






# async def process_new_message(message):
#     if message is None:
#         print("Received None message. Skipping processing.")
#         return
    
#     if 'time zone' in message.lower():
#         signal_info = extract_signal_info(message)
#         if signal_info:
#             print("Start Time:", signal_info["Start Time"])
#             mini = signal_info["Start Time"].split(":")
#             asset = signal_info["Currency Pair"]
#             direction = signal_info["Position"]
#             minute = int(mini[1])

#             current_time = datetime.now()
#             current_minute = current_time.minute
#             minute_difference = minute - current_minute

#             if minute_difference > 15:
#                 print("Difference is greater than 15 minutes. Skipping trade.")
#                 return
#             if minute_difference < 0:
#                 print("Specified time is in the past. Skipping trade.")
#                 return

#             start_time = current_time.replace(hour=current_time.hour, minute=minute, second=0, microsecond=0)
#             print("Current time:", current_time)
#             print("Start time:", start_time)

#             await handle_trade(asset, direction)

# async def handle_trade(asset, direction):
#     check_connect, message = await connect()
#     if check_connect:
#         amount = int(await client.get_balance() * 0.01)
#         asset_query = asset_parse(asset)
#         asset_open = await client.check_asset_open(asset_query)
#         if asset_open[2]:
#             print("OK: Asset is open.")
#             status, buy_info = await client.buy(amount, asset, direction, duration)
#             print(status, buy_info)
#         else:
#             print("ERROR: Asset is closed.")
#         print("Current balance: ", await client.get_balance())
#     print("Leaving...")
#     await client.close()

# async def main():
#     client = TelegramClient('session_name', int(env_vars['API_ID']), env_vars['API_HASH'])
#     await client.start()
#     entity = await client.get_entity(-1002009134814)  # Replace with your channel ID

#     @client.on(events.NewMessage(chats=entity))
#     async def handler(event):
#         await process_new_message(event.message.text)

#     print(f"Listening for new messages in channel: {entity.title}")
#     await client.run_until_disconnected()

# # Run the asynchronous function
# asyncio.run(main())

# async def make_trade(asset, direction, duration, start_time, amount):
#     check_connect, message = await connect()
#     if check_connect:
#         print("Current balance: ", await client.get_balance())

#         asset_query = client.asset_parse(asset)
#         asset_open = client.check_asset_open(asset_query)

#         if asset_open[2]:
#             print("OK: Asset is open.")

#             for i in range(3):   # Try thrice at most
#                 status, buy_info = await client.buy(amount, asset, direction, duration)
#                 print(status, buy_info)

#                 if status:
#                     print("Awaiting result...")

#                     if await client.check_win(buy_info["id"]):
#                         print(f"\nWin!!! \nNice, we won!!!\nProfit: R$ {client.get_profit()}")
#                         break
#                     else:
#                         print(f"\nLoss!!! \nOops, we lost!!!\nLoss: R$ {client.get_profit()}")
#                         amount *= 2   # double the amount and try again

#                 else:
#                     print("Operation failed!!!")

#         else:
#             print("ERROR: Asset is closed.")
        
#         print("Current balance: ", await client.get_balance())

#         print("Exiting...")
#         client.close()

# # async def trade_data(data):

    

# async def main():
#     # Set up Telegram client
#     client = TelegramClient('session_name', int(env_vars['API_ID']), env_vars['API_HASH'])

#     # Connect to Telegram API
#     await client.start()

#     # Define the Telegram entity (channel, group, etc.) to listen to
#     entity = await client.get_entity(-1002009134814)  # Replace with your channel ID

#     # Listen for new messages in the channel and process them
#     @client.on(events.NewMessage(chats=entity))
#     async def handler(event):
#         await process_new_message(event.message.text)

#     print(f"Listening for new messages in channel: {entity.title}")
#     await client.run_until_disconnected()

# # Run the asynchronous function
# asyncio.run(main())



import asyncio
from main import *

async def main():
    await buy_and_check_win_3()

if __name__ == "__main__":
    asyncio.run(main())
