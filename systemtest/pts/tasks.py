# Python
from typing import Any, Union

# Django
from django.db.models import Q
from django.conf import settings

# Celery
from config.celery_app import app

# APPs
from systemtest.utils.db2 import Database
from systemtest.pts import models as pts_models

database = Database(**settings.DATABASES.get("db2"))


def get_pending_request():
    return pts_models.Request.objects.filter(request_status__name="PENDING")


def get_bad_request():
    return pts_models.Request.objects.filter(request_status__name="BAD")


def get_ncm(request: pts_models.Request) -> Union[dict[str, str], None]:
    data = {
        "part_number": request.part_number,
        "serial_number": request.serial_number,
        "created": request.created
    }

    sql = """
        SELECT
            RPREJS AS NCM_TAG,
            RPCULC AS CURRENT_LOCATION
        FROM
            QRYQ.MFSGPRP10_GRC
        WHERE
            RPITEM = '00000{part_number}' AND   -- Part number has 12 chars,
                                                -- 5 chars aditional to save in db,
                                                -- so filled extra chars with 0s
            RPPTSN = '{serial_number}' AND
            RPSTMP > '{created}';
    """.format(**data)

    rows = database.fetch(sql)
    row = next(rows, {})

    print(data)
    print(row)

    if ncm_tag := row.get("NCM_TAG"):
        data["ncm_tag"] = ncm_tag

        row = next(rows, {})
        data["is_returned"] = row.get("CURRENT_LOCATION", "").strip() == "PNCM"

        return data
    return None


def return_bad(request: pts_models.Request, ncm_data: dict[str, Any]):
    if ncm_data:
        bad_status = pts_models.RequestStatus.objects.get(
            name="BAD")

        if request.request_status != bad_status:
            request.__dict__.update(ncm_data)
            request.save()

        if ncm_data.get("is_returned"):
            request.request_status = pts_models.RequestStatus.objects.get(
                name="CLOSE BAD")
            request.save()


@app.task()
def looking_bad():
    for pending_request in get_pending_request():
        if ncm_data := get_ncm(pending_request.get_first_request()) is None:
            ncm_data = get_ncm(pending_request)
        return_bad(pending_request, ncm_data)

    for bad_part in get_bad_request():
        ncm_data = get_ncm(bad_part)
        return_bad(bad_part, ncm_data)
