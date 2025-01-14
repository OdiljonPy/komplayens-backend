import re
import random
from datetime import timedelta, datetime

from exceptions.error_messages import ErrorCodes
from exceptions.exception import CustomApiException
from utils.send_otp_code import send_otp_code


def phone_number_validation(value):
    if not re.match(pattern=r'^\+998\d{9}$', string=value):
        raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Phone number is invalid.')


def is_user_created(request):
    from .models import User
    data = request.data
    if 'phone_number' in data:
        user = User.objects.filter(phone_number=data.get('phone_number')).exclude(id=request.user.id).first()
        return user
    return


def gen_otp_code():
    return str(random.randint(a=100000, b=999999))


def check_block_user(user_id):
    from .models import OTP
    otp = OTP.objects.filter(user_id=user_id).first()
    if not otp.created_at < datetime.now() - timedelta(hours=5):
        return False
    return True


def otp_create(user_id):
    from .models import OTP

    otp_count = OTP.objects.filter(user_id=user_id).count()
    if otp_count and otp_count > 2 and not check_block_user(user_id):
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Too many attempts, please try again later.')

    last_otp = OTP.objects.filter(user_id=user_id).first()
    if last_otp and last_otp.created_at + timedelta(minutes=2) > datetime.now():
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='OTP is not expired.')

    if otp_count and otp_count > 2 and check_block_user(user_id):
        OTP.objects.filter(user_id=user_id).delete()

    otp_code = gen_otp_code()
    otp = OTP.objects.create(user_id=user_id, otp_code=otp_code)
    send_otp_code(otp)
    return str(otp.otp_key)


def otp_verification(data):
    from .models import OTP
    otp = OTP.objects.filter(otp_key=data.get('otp_key')).first()
    if not otp:
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='OTP key is invalid')

    if otp.request_count > 2:
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='Too many attempts.')

    if otp.created_at + timedelta(minutes=2) < datetime.now():
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='OTP code is expired')

    if otp.otp_code != data.get('otp_code'):
        otp.request_count = (otp.request_count + 1)
        otp.save(update_fields=['request_count'])
        raise CustomApiException(ErrorCodes.INVALID_INPUT, message='OTP code is invalid')

    OTP.objects.filter(user_id=otp.user_id).delete()
    return otp.user_id


def create_customer(request):
    from .models import Customer
    user_agent = request.META.get('HTTP_USER_AGENT')
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
    ip_address = ip_address or request.META.get('REMOTE_ADDR')
    customer = Customer.objects.filter(ip_address=ip_address, user_agent=user_agent).first()
    if customer:
        return customer
    customer = Customer.objects.create(ip_address=ip_address, user_agent=user_agent)
    return customer
