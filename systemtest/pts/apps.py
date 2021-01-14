from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PtsConfig(AppConfig):
    name = "systemtest.pts"
    verbose_name = _("PTS")

    def ready(self):
        try:
            import systemtest.pts.signals  # noqa F401
        except ImportError:
            pass
