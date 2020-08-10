import requests

with open("SECRET_API_TOKEN", "r") as token_file:
    secret_api_token = token_file.read().strip()
print("Secret_token: " + secret_api_token)

def telegram_bot_sendtext(bot_message):
    bot_token = secret_api_token
    bot_chatID = '13225322'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    print("Request: " + send_text)
    response = requests.get(send_text)

    return response.json()

test = telegram_bot_sendtext("Test shit")
print(test)

