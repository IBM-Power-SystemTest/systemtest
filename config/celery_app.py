import os

from celery import Celery

# set the default Django settings module for the "celery" program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("systemtest")

# Using a string here means the worker doesn"t have to serialize
# the configuration object to child processes.
# - namespace="CELERY" means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Scheduler
app.conf.beat_schedule = {
    "Fetch_quality_db_every_6_min": {
        "task": "quality.fetch_database",
        "schedule": 60.0*6,
    },
}
