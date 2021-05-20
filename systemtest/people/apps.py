"""
App config
    References:
        https://docs.djangoproject.com/en/3.1/ref/applications/
"""

from django.apps import AppConfig

class PeopleConfig(AppConfig):
    name = "systemtest.people"
    verbose_name = "People Managment"

    def ready(self):
        try:
            import systemtest.people.signals  # noqa F401
        except ImportError:
            pass
