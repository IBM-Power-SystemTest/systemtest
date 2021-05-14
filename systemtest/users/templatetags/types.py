"""
Custom Django TemplaTags for Users templates,
template tags to handle python type like lists, zip objects, define a var
    References:
        https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
"""

from typing import Any
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
