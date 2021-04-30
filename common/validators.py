from django.core.exceptions import ValidationError
import re


def mobile_validator(mobile):
    if mobile[0:2] != '09':
        raise ValidationError('Please follow the mentioned format: 09********')
    try:
        mobile = int(mobile)
    except ValueError:
        raise ValidationError('Invalid value!')



def mobile_length_validator(mobile):
    if len(mobile) != 11:
        raise ValidationError('Invalid length!')


def validate_not_empty(value):
    if value == '':
        raise ValidationError('{} is empty!'.format(value))


def email_regex_validator(email):
    EMAIL_REGEX = re.compile(r'^[a-z]+[a-zA-Z0-9.+_-]*@[a-zA-Z0-9]+.[a-zA-Z]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(email):
        raise ValidationError('Invalid Email Address!')
