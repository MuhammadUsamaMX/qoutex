import socket
import json
import asyncio
from trade import trade, get_signal_data
from termcolor import colored
from wait_until_time import wait_until_time
from dotenv import dotenv_values
from multiprocessing import Process, Queue

# Load environment variables
env_vars = dotenv_values('.env')

async def preprocess_and_validate_signal(signal):
    try:
        return True, signal
    except Exception as e:
        print(f"Error during signal validation: {e}")
        return False, None

async def handle_signal(connection, signal_queue):
    try:
        buffer = ""
        while True:
            data = connection.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8')

            print(colored("Buffer before JSON parsing: " + buffer, "yellow"))

            try:
                signal = json.loads(buffer)
                print(colored("Received signal: " + json.dumps(signal, indent=2), "magenta"))
                buffer = "" # Reset buffer after successful parse

                valid, processed_signal = await preprocess_and_validate_signal(signal)
                if valid:
                    action_color = "green" if signal['Position'] == 'CALL' else "red"
                    print(colored("Valid signal received. Processing...", "blue"))
                    print(colored(f"Processed Signal: {processed_signal}", action_color))

                    _duration = 5
                    _action = signal["Position"].lower()
                    _amount = 50
                    _asset = signal["pair"]

                    on_time = await wait_until_time(signal['time'])

                    if on_time:
                        win = await trade(
                            duration=_duration,
                            action=_action,
                            amount=_amount,
                            asset=_asset
                        )
                        if not win:
                            print(colored("Entering First TP"), "yellow")
                            win = await trade(
                                duration=_duration,
                                action=_action,
                                amount=_amount*2,
                                asset=_asset
                            )
                            if not win:
                                print(colored("Entering Second TP"), "yellow")
                                win = await trade(
                                    duration=_duration,
                                    action=_action,
                                    amount=_amount*4,
                                    asset=_asset
                                )
                    print(colored("Consumer [INFO]: Sleeping for 5 seconds...", "blue"))
                    await asyncio.sleep(5)
                else:
                    print(colored("Invalid signal received. Ignoring...", "red"))
                    buffer = ''

            except json.JSONDecodeError:
                print(colored("Failed to decode JSON, waiting for more data...", "red"))
                buffer = ''
                continue

    finally:
        connection.close()

async def run_get_signal_data(signal_queue):
    while True:
        signal_data = await get_signal_data()
        signal_queue.put(signal_data)

def process_connection(client_socket, signal_queue):
    asyncio.run(handle_signal(client_socket, signal_queue))

def process_get_signal_data(signal_queue):
    asyncio.run(run_get_signal_data(signal_queue))

async def main():
    signal_queue = Queue()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as consumer_socket:
        consumer_socket.bind(('localhost', int(env_vars['PORT'])))
        consumer_socket.listen(1)
        print(colored("Waiting for connection on port 9999...", "cyan"))

        # Start the process for get_signal_data
        signal_data_process = Process(target=process_get_signal_data, args=(signal_queue,))
        signal_data_process.start()

        while True:
            connection, client_address = consumer_socket.accept()
            print(colored(f"Connected to {client_address}", "green"))

            # Start a new process for each connection
            process = Process(target=process_connection, args=(connection, signal_queue))
            process.start()

if __name__ == "__main__":
    asyncio.run(main())