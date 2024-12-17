import requests
from datetime import timedelta
from django.conf import settings


def send_otp_code(otp):
    text = (
        f"P/j: Komplayens\n"
        f"User: {otp.user_id}\n"
        f"OTP_code: {otp.otp_code}\n"
        f"OTP_key: {otp.otp_key}\n"
        f"Expire in: {(otp.created_at + timedelta(minutes=2)).strftime('%Y-%m-%d %H:%M:%S')}\n")
    requests.post(
        url=f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
        data={'chat_id': settings.TELEGRAM_CHANNEL_ID, 'text': text}
    ).json()
