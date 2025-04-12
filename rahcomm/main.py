#!/usr/bin/python3

import pyrah
import threading
import argparse
import readline
import os
import atexit

parser = argparse.ArgumentParser(description="RAH Communication Tool")
parser.add_argument("--appid", type=int, default=3, help="Application ID (default: 3)")
args = parser.parse_args()

APP_ID = args.appid
DATA_LENGTH = 6

home_dir = os.path.expanduser('~')
history_file = os.path.join(home_dir, '.rahcomm.hist')

if not os.path.exists(history_file):
    with open(history_file, 'a') as f:
        pass

readline.parse_and_bind('set editing-mode vi')
readline.read_history_file(history_file)

history = []

def save_history():
    with open(history_file, 'a') as f:
        for entry in history:
            f.write(entry + '\n')

atexit.register(save_history)

def rah_writer():
    try:
        while True:
            user_input = input("RAH WRITE: ")

            try:
                hex_values = [int(value, 16) for value in user_input.split()]
                pyrah.rah_write(APP_ID, bytes(hex_values))
            except ValueError:
                print("Invalid input.")
            else:
                history.append(user_input)
    except EOFError:
        pass
    except Exception as error:
        print(f"\nWrite Error: {error}")

def rah_reader():
    try:
        while True:
            try:
                received_data = pyrah.rah_read(APP_ID, DATA_LENGTH)
                print(f"\nRAH  READ: {received_data.hex(' ')}")
            except Exception as error:
                print(f"Read Error: {error}")
    except Exception as error:
        print(f"Read Error: {error}")

def main():
    try:
        print("<<<<<<<<<<< RAH Communication >>>>>>>>>")
        print(f"Using APP ID: {APP_ID}")
        read_thread = threading.Thread(target=rah_reader, daemon=True)
        write_thread = threading.Thread(target=rah_writer, daemon=True)
        
        read_thread.start()
        write_thread.start()

        write_thread.join()
        read_thread.join(0)
    except KeyboardInterrupt:
        print("\nClosing application...")
    except Exception as error:
        print(f"Application Error: {error}")

if __name__ == "__main__":
    main()
