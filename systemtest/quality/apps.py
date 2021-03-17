from django.apps import AppConfig

class QualityConfig(AppConfig):
    name = "systemtest.quality"
    verbose_name = "Quality"

    def ready(self):
        try:
            import systemtest.quality.signals  # noqa F401
        except ImportError:
            pass
