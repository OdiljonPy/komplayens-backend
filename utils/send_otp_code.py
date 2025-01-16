import requests
from datetime import timedelta
from django.conf import settings


def send_otp_code(passwd):
    text = passwd
    requests.post(
        url=f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
        data={'chat_id': settings.TELEGRAM_CHANNEL_ID, 'text': text}
    ).json()
