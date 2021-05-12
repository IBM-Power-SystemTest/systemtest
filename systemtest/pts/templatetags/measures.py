"""
Django custom TemplaTags for PTS templates,
template tags to handler some calcs like time elapsed between to datetimes
    References:
        https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
"""

# Python
from datetime import datetime, timedelta
from typing import Literal

# Django
from django.template import Library

register = Library()


@register.filter("get_shift")
def get_shift(date: datetime) -> Literal["1", "2", "3", "?"]:
    """
    According to the time, it is assigned the shift
    07:00 - 14:59 = 1
    15:00 - 22:59 = 2
    23:00 - 06:59 = 3

    Args:
        date:
            Python datetime, extract the hour an eval

    Returns:
        Return a string with the corresponding shift; 1,2,3 or ?
    """

    try:
        hour = date.hour
    except AttributeError:
        # If date is not datetime like None or str set hour to -1
        hour = -1

    # By default shift is equal to ? and override in the conditional block
    shift = "?"

    if hour >= 7 and hour <= 14:
        shift = "1"
    elif hour >= 15 and hour <= 22:
        shift = "2"
    elif (hour >= 0 and hour <= 7) or hour >= 23:
        shift = "3"

    return shift


@register.filter
def elapsed_time_min(time: datetime) -> int:
    """
    Gets the number of minutes elapsed from a time to now

    Args:
        time:
            Python DateTime to calculate the elapsed time

    Returns:
        Integer number of minutes elapsed from the past date to now

        example:
            40
    """

    now = datetime.now()
    delta = timedelta(minutes=1)

    return (now - time) // delta
