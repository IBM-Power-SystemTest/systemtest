"""
Quality app config
    References:
        https://docs.djangoproject.com/en/3.1/ref/applications/
"""

from django.apps import AppConfig


class QualityConfig(AppConfig):
    name = "systemtest.quality"
    verbose_name = "Quality"

    def ready(self):
        try:
            import systemtest.quality.signals  # noqa F401
        except ImportError:
            pass
