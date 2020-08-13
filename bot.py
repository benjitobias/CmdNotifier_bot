#!/bin/python
import os
import time
import urllib
import argparse
import requests

package_dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
   
parser.add_argument('-p', '--pid', dest='pid', action='store', help="PID to monitor")

args = parser.parse_args()

with open(os.path.join(package_dir, "SECRET_API_TOKEN"), "r") as token_file:
    secret_api_token = token_file.read().strip()
print("Secret_token: " + secret_api_token)

def telegram_bot_sendtext(bot_message):
    bot_token = secret_api_token
    bot_chatID = '13225322'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    print("Request: " + send_text)
    response = requests.get(send_text)

    return response.json()

if args.pid:
    pid = args.pid
    with open("/proc/%s/cmdline" % pid) as cmd_file:
        cmd = cmd_file.read().replace("\x00", " ")
    print("Monitoring: " + str(pid) + " : " + cmd)

    while True:
        if not os.path.exists("/proc/%s" % pid):
            test = telegram_bot_sendtext("%s finished running on " % urllib.parse.quote(cmd) + os.uname()[1])
            break
        time.sleep(3)



else:
    test = telegram_bot_sendtext("Process finished running on " + os.uname()[1])

print(test)

