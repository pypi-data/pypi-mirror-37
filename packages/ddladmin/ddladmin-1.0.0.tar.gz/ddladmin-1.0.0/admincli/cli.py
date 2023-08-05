import os
import signal
import sys
import argparse

from admincli.api import *
from admincli.help import *
from admincli.parse import *

cred = None
api = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

def message_box(messages):
    print("*" * 80)
    print("**" + " " * 76 + "**")
    for line in messages:
        length = len(line)
        space_left = (76 - length) // 2
        space_right = 76 - length - space_left
        print("**{}{}{}**".format(" " * space_left, line, " " * space_right))

    print("**" + " " * 76 + "**")
    print("*" * 80)
    return

def goodbye(sig, frame):
    clear_screen()
    global cred
    global api
    message_box(['Thank you for using Distributed Deep Learning Admin Portal'])
    if cred is not None:
        api.logout(cred)
    sys.exit(0)
    return

def welcome():
    clear_screen()
    welcome_lines = [
        "Welcome to Distributed Deep Learning Admin Portal",
        "Type '{}' for help".format(CMD_HELP),
        "Press 'Ctrl-C' to exit"
    ]
    message_box(welcome_lines)
    return

def get_prompt(cred):
    prompt = ">>> "
    if cred["account_data"]["is_super_admin"]:
        user = "(Super Admin)"
    else:
        user = "(Admin)"
    return "{} {}".format(user, prompt)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--master_endpoint_override',
        type=str,
        help='override to master server url')

    parser.add_argument(
        '--access_id',
        type=str,
        help='access id to log in to the admin portal')

    parser.add_argument(
        '--password',
        type=str,
        help='password to log in to the admin portal')

    parser.add_argument(
        '--command',
        type=str,
        help='command to execute')

    FLAGS, _ = parser.parse_known_args()
    if FLAGS.master_endpoint_override is None:
        master_endpoint = "http://dtf-masterserver-dev.us-west-1.elasticbeanstalk.com"
    else:
        master_endpoint = FLAGS.master_endpoint_override

    admin_id = None
    if FLAGS.access_id is not None:
        admin_id = FLAGS.access_id

    admin_password = None
    if FLAGS.password is not None:
        admin_password = FLAGS.password

    command = None
    if FLAGS.command is not None:
        command = FLAGS.command

    # Register for crtl-c
    signal.signal(signal.SIGINT, goodbye)
    if command is None:
        # Print Welcome message...
        welcome()
    global cred
    global api
    api = MasterServerApi(master_endpoint)
    print("Connect to: {}".format(master_endpoint))
    while True:
        if cred is None:
            if admin_id is None:
                admin_id = input("Access Id: ")
            if admin_password is None:
                admin_password = input("Password: ")
            cred = api.login(admin_id, admin_password)
            if cred is None:
                continue
        else:
            # Wait for console input...
            if command is None:
                console_input = input(get_prompt(cred))
            else:
                console_input = command

            console_input_splits = console_input.split(";")
            for console_input_split in console_input_splits:
                commands = console_input_split.split()
                if len(commands) == 0:
                    continue
                elif commands[0].lower() == CMD_HELP:
                    help(commands)
                elif commands[0].lower() == CMD_LOGOUT:
                    api.logout(cred)
                    clear_screen()
                    message = ["You Have Been Logged Out"]
                    message_box(message)
                    admin_id = None
                    admin_password = None
                    cred = None
                else:
                    query(api, cred, console_input_split)
            if command is not None:
                if api is not None and cred is not None:
                    api.logout(cred)
                return