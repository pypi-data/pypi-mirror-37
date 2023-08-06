import re

from django.conf import settings
from django.core.exceptions import ValidationError


def phone_number(value, pattern):
    str_value = "%s" % (value)
    pattern = pattern or '^[0-9+\(\)#\.\s\/ext-]+$'
    p = re.compile(pattern)
    if not p.match(str_value):
        raise ValidationError(u'Invalid format.')


def CellNumber(value):
    """
        sample for BW:
            CELLPHONE_REGEX = '^[7]{1}[12345678]{1}[0-9]{6}$'
    """
    try:
        pattern = settings.CELLPHONE_REGEX
    except AttributeError:
        pattern = None
    phone_number(value, pattern)


def TelephoneNumber(value):
    """
        sample for BW:
            TELEPHONE_REGEX = '^[2-8]{1}[0-9]{6}$'
    """
    try:
        pattern = settings.TELEPHONE_REGEX
    except AttributeError:
        pattern = None
    phone_number(value, pattern)
