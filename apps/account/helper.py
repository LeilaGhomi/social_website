from django.utils import timezone

from kavenegar import *

from apps.account.models import User
from social_website.settings import Kavenegar_API
from random import randint


def send_otp(mobile, otp):
    mobile = [mobile, ]
    try:
        api = KavenegarAPI(Kavenegar_API)
        params = {
            'sender': '1000596446',
            'receptor': mobile,
            'message': 'Your OTP is {}'.format(otp),
        }
        response = api.sms_send(params)
        print('OTP: ', otp)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def get_random_otp():
    return randint(10000, 99999)


def check_otp_expiration(mobile):
    try:
        user = User.objects.get(phone_number=mobile)
        now = timezone.now()
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        print('OTP TIME: ', diff_time)

        if diff_time.seconds > 120:
            return False
        return True

    except User.DoesNotExist:
        return False
