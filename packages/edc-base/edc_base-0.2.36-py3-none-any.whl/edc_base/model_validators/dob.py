import arrow

from django.core.exceptions import ValidationError
from django.utils.timezone import get_default_timezone

from ..exceptions import FutureDateError

from .date import date_not_future


def dob_not_future(value):
    """this is unreliable as the DoB is more likely relative to something like the report_datetime
    and not today."""
    try:
        date_not_future(value)
    except FutureDateError:
        raise FutureDateError(
            u'Date of birth cannot be a future date. You entered {}.'.format(value))


def dob_not_today(value):
    """this is unreliable as the DoB is more likely relative to something like the report_datetime
    and not today."""
    value_utc = arrow.Arrow.fromdate(
        value, tzinfo=get_default_timezone()).to('utc').date()
    if value_utc == arrow.utcnow().date:
        raise ValidationError(
            u'Date of birth cannot be today. You entered {}.'.format(value))
