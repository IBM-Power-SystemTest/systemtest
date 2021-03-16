from datetime import datetime, timedelta
from django.template import Library

register = Library()


@register.filter("get_shift")
def get_shift(date: datetime) -> str:
    hour = date.hour
    if hour >= 7 and hour <= 14:
        return "1"
    elif hour >= 15 and hour <= 22:
        return "2"
    elif (hour >= 0 and hour <= 7) or hour >= 23:
        return "3"
    else:
        return "?"


@register.filter
def elapsed_time_min(time: datetime) -> int:
    now = datetime.now()
    delta = timedelta(minutes=1)
    return (now - time) // delta
