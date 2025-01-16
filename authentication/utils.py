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
