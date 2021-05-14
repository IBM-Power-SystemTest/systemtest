# Django
from django.db.models import Q

# Celery
from config.celery_app import app

# APPs
from systemtest.quality import forms as quality_forms, models as quality_models
from systemtest.quality.utils.models import fetch_database


@app.task()
def sync_database() -> dict[str, int]:
    quality_system = quality_models.QualitySystem.objects

    query = Q(operation_status="W")
    waiting_systems = quality_system.filter(query).values("workunit")

    len_systems = 0
    for row in fetch_database():
        quality_system.update_or_create(**row)
        waiting_systems = waiting_systems.exclude(workunit=row.get("workunit"))

        len_systems += 1

    count_dict = {"FECTH": len_systems}

    for workunit in waiting_systems:
        system = quality_system.get(**workunit)
        system.operation_status = "A"
        system.save()

    count_dict["REMOVED"] = len(waiting_systems)
    return count_dict
