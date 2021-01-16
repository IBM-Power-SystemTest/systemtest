from django.apps import AppConfig

class PtsConfig(AppConfig):
    name = "systemtest.pts"
    verbose_name = "PTS"

    def ready(self):
        try:
            import systemtest.pts.signals  # noqa F401
        except ImportError:
            pass
