import asyncio
from datetime import datetime
from termcolor import colored

async def wait_until_time(time):
    differance = 3
    while True:
        current_time = datetime.now()
        remaining_seconds = (time - current_time.minute - 1) * 60 + (60 - current_time.second)
        if remaining_seconds <= differance:  # Also start before differance seconds
            try:
                return True
            except Exception as e:
                print("While executing trade, Error occurred:", e)
                return False
        # print(f"\r{remaining_seconds-differance} remaining seconds left to start trade", end="")
        print(colored(f"\r{remaining_seconds - differance} remaining seconds left to start trade", "green"), end="")
        await asyncio.sleep(1)
    print("\n")