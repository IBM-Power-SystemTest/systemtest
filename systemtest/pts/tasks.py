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


def get_ncm(pending_part: pts_models.Request) -> Union[dict[str, str], None]:
    data = {
        "part_number": pending_part.part_number,
        "serial_number": pending_part.serial_number,
        "created": pending_part.created
    }

    sql = """
        SELECT
            RPREJS AS NCM_TAG
        FROM
            QRYQ.MFSGPRP10_GRC
        WHERE
            RPCULC = 'PDBG' AND
            RPITEM = '00000{part_number}' AND   -- Part number has 12 chars,
                                                -- 5 chars aditional to save in db,
                                                -- so filled extra chars with 0s
            RPPTSN = '{serial_number}' AND
            RPSTMP > '{created}';
    """.format(**data)

    rows = database.fetch(sql)
    row = next(rows, {})

    if ncm_tag := row.get("NCM_TAG"):
        data["ncm_tag"] = ncm_tag
        del data["created"]
        return data

    return None


@app.task()
def return_ncm():
    query = (
        Q(request_status__name="PENDING") |
        Q(request_status__name="INSTALADO EN OTRA WU") |
        Q(request_status__name="REVISION CON EL ME")
    )

    for pending_part in pts_models.Request.objects.filter(query):
        if ncm_data := get_ncm(pending_part.get_first_request()) is None:
            ncm_data = get_ncm(pending_part)

        if ncm_data:
            pending_part.__dict__.update(ncm_data)
            pending_part.request_status = pts_models.RequestStatus.objects.get(
                name="BAD")

            pending_part.save()
