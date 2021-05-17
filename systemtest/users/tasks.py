"""
Celery task for Users app, registry of task and configure in database

    refences:
        https://docs.celeryproject.org/en/v4.4.7/userguide/tasks.html
        https://docs.celeryproject.org/en/v4.4.7/userguide/periodic-tasks.html
        https://github.com/celery/celery/blob/master/examples/django/demoapp/tasks.py
"""
# Python
from datetime import date

# Django
from django.contrib.auth import get_user_model
from django.conf import settings

# Celery
from config.celery_app import app

# APPs
from systemtest.utils.utils import dict_counter


@app.task()
def looking_inactive() -> dict[str, int]:
    count_dict = {}
    for user in get_user_model().objects.all():
        dict_counter(count_dict, "USERS")
        last_password_date = user.last_password_modified
        password_days_delta = (date.today() - last_password_date).days

        if password_days_delta >= settings.PASSWORD_EXPIRE_DAYS:
            user.is_active = False
            user.save()
            dict_counter(count_dict, "DEACTIVATED")

    return count_dict
