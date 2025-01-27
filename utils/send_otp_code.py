import time
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth


def send_password(message: str, recipient: str, user_id: int):
    url = f"{settings.SMS_BASE_URL}/send"
    message_id = f"yurins{user_id}{int(time.time())}"
    messages = {
        "messages":
            [
                {"recipient": recipient,
                 "message-id": message_id,
                 "sms": {
                     "originator": "3700",
                     "content": {
                         "text": message}
                 }
                 }
            ]
    }
    resp = requests.post(
        url=url,
        auth=HTTPBasicAuth(settings.SMS_USERNAME, settings.SMS_PASSWORD),
        json=messages
    )
    print('=' * 50, "SMS", '=' * 50, )
    print('-' * 50, 'json', '-' * 50, )
    print(messages)
    print('-' * 50, 'json', '-' * 50, )
    print(resp)
    print('=' * 50, "SMS", '=' * 50, )
