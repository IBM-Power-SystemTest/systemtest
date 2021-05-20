"""
Custom Django TemplaTags for Users templates,
template tags to handle groups
    References:
        https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
"""

# Django
from django.template import Library

# APPs
from systemtest.users.models import User

register = Library()


@register.filter("has_group")
def has_group(user: User, group_name: str) -> bool:
    """
    Checks if user has a specific group
        References:
            https://docs.djangoproject.com/en/3.1/topics/db/queries/

    Args:
        user:
            Users to check if they have the group
        group_name:
            Name of the group to search

    Returns:
        If user have the group return True else return False
    """
    return user.groups.filter(name=group_name).exists()
