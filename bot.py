#!/bin/python
import os
import time
import json
import urllib
import argparse
import requests


BOT_TOKEN = "bot_token"
CHAT_ID = "chat_id"

BOT_SEND_TEXT_REQUEST = "https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={text}"

PROC_PID = "/proc/{pid}"
PROC_CMDLINE = "/proc/{pid}/cmdline"

PID_MESSAGE = "{cmd} finished running on {hostname}"

package_dir = os.path.dirname(os.path.realpath(__file__))

default_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")

parser = argparse.ArgumentParser()
   
parser.add_argument('-p', '--pid', dest='pid', action='store', help="PID to monitor", type=str)
parser.add_argument('-c', '--config', dest='config', action='store', help="Config file", default=default_config_path)
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="Config file", default=default_config_path)

args = parser.parse_args()

def monitor_pid(pid, bot_token, chat_id):
    with open(PROC_CMDLINE.format(pid=pid)) as cmd_file:
        cmd = cmd_file.read().replace("\x00", " ")
    print("Monitoring: " + pid + " : " + cmd)

    while True:
        if not os.path.exists(PROC_PID.format(pid=pid)):
            text = PID_MESSAGE.format(cmd=cmd, hostname=os.uname()[1])
            response = send_telegram_bot_message(bot_token, chat_id, text)
            break
        time.sleep(3)


def read_config(config_path):
    with open(config_path) as config_file:
        config = json.load(config_file)
    return config


def send_telegram_bot_message(bot_token, chat_id, text):
    verbose_print("Message to send: %s" % text)
    url_text = urllib.parse.quote(text)
    bot_request = BOT_SEND_TEXT_REQUEST.format(bot_token=bot_token, chat_id=chat_id, text=url_text)
    verbose_print("Request: %s" % bot_request)
    response = requests.get(bot_request).json()
    verbose_print("Respnse: %s" % response)
    return response


def verbose_print(text):
    if args.verbose:
        print(text)


def main():
    args = parser.parse_args()
    config = read_config(args.config)

    bot_token = config[BOT_TOKEN]
    chat_id = config[CHAT_ID]

    if args.pid:
        monitor_pid(args.pid, bot_token, chat_id)
    else:
        text = "Command finished running on {hostname}".format(hostname=os.uname()[1])
        send_telegram_bot_message(bot_token, chat_id, text)
    

if __name__ == '__main__':
    main()

