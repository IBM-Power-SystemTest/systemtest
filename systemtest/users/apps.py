"""
Users app config
    References:
        https://docs.djangoproject.com/en/3.1/ref/applications/
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "systemtest.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import systemtest.users.signals  # noqa F401
        except ImportError:
            pass
