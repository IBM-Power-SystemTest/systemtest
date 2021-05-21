"""
Custom Django TemplaTags for Users templates,
template tags to handle python type like lists, zip objects, define a var
    References:
        https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
"""

from typing import Any, Literal
from datetime import datetime, timedelta

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def to_list(*args) -> tuple:
    """
    Recives a positional args expanded and return it in list format

    Args:
        args:
            Positional args expanded

    Returns:
        Compacted positional args (tuple)
    """

    return args


@register.simple_tag
def define(val: str = "") -> str:
    """
    Sets a value in Django template

    Args:
        val

    Returns:
        Values passed in args
    """
    return val


@register.filter(name="zip")
def zip_lists(a: list, b: list):
    """
    Zip two list of same lenght

    Args:
        a:
            First list
        b:
            Second list

    Returns:
        Both list zipped
    """
    return zip(a, b)


@register.simple_tag
def get_setting(name: str) -> Any:
    return getattr(settings, name, "")


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.filter(name="delta_days")
def delta_days(start_datetime: datetime, days: int, op_sum: bool = True) -> datetime:
    delta = timedelta(days=days) if op_sum else -timedelta(days=days)
    return start_datetime + delta


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
