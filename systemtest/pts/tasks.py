"""
Celery task for PTS app, registry of task and configure in database

    refences:
        https://docs.celeryproject.org/en/v4.4.7/userguide/tasks.html
        https://docs.celeryproject.org/en/v4.4.7/userguide/periodic-tasks.html
        https://github.com/celery/celery/blob/master/examples/django/demoapp/tasks.py
"""

# Python
from typing import Any

# Django
from django.conf import settings

# Celery
from config.celery_app import app

# APPs
from systemtest.utils.db2 import Database
from systemtest.pts.utils.models import *


@app.task()
def looking_bad() -> dict[str, int]:
    """
    Checks all parts with status PENDING and BAD looking for ncm data and location

    Args:
        None

    Returns:
        None
    """

    # Create DB config
    database = Database(**settings.DATABASES.get("db2"))

    # Get status to move Request
    bad_status = get_status("BAD")
    close_bad_status = get_status("CLOSE BAD")

    # Create a function to handle a ncm_data and Request status
    def return_bad(request: pts_models.Request, ncm_data: dict[str, Any]) -> None:
        """
        Updates the Request data and moves it state as the case may be

        Args:
            request:
                Request object to update ncm data
            ncm_data:
                Dict with ncm data (Request data to update must be the
                same as the dictionary keys and may carry additional keys)

        Returns:
            None, update and save Request object inline
        """
        if ncm_data:
            # If Request has ncm_data and status is different of BAD move
            # to BAD and fill ncm_data, like pn, sn, ncm_tag and status
            if request.request_status != bad_status:
                request.__dict__.update(ncm_data)
                request.request_status = bad_status
                request.save()

            # If ncm_data 'is returned' ( which means that the location of
            # the part is PNCM } close part. NCM data was previously added
            # if you didn't have it before
            if ncm_data.get("is_returned"):
                request.request_status = close_bad_status
                request.save()

    count = 0

    # Cheking the parts that are PENDING, both the part that was ordered
    # and the last part registered
    for pending_request in get_request_by_status_name("PENDING"):
        if ncm_data := get_ncm(pending_request.get_first_request(), database):
            ncm_data = get_ncm(pending_request, database)
            count += 1
        return_bad(pending_request, ncm_data)

    count_dict = {"FROM PENDING": count}
    count = 0

    # Cheking the parts that are BAD, especially the locality of this,
    # which is PNCM to move to the next state
    for bad_part in get_request_by_status_name("BAD"):
        ncm_data = get_ncm(bad_part, database)
        count += 1
        return_bad(bad_part, ncm_data)

    database.close()

    count_dict["FROM RETURN"] = count
    return count_dict
