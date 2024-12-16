import re
import random
from .models import OTP
from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes


def phone_number_validation(value):
    if not re.match(pattern=r'^\+998\d{9}$', string=value):
        raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Phone number is invalid.')


def gen_otp_code():
    return str(random.randint(a=100000, b=999999))


def create_otp(user_id):
    otp_code = gen_otp_code()
    otp = OTP.objects.create(user_id=user_id, otp_code=otp_code)
    return str(otp.otp_key)


def check_otp(data):
    otp = OTP.objects.filter(otp_key=data.get('otp_key')).first()
    if not otp:
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='OTP key is invalid')

    if otp.otp_code != data.get('otp_code'):
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='OTP code is invalid')
    count = OTP.objects.filter(user_id=otp.user_id).count()
    if count > 3:
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Too many attempts')
    return
