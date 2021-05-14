# Django
from django.db.models import Q
from django.db.utils import IntegrityError

# Celery
from config.celery_app import app

# APPs
from systemtest.quality import forms as quality_forms, models as quality_models
from systemtest.quality.utils.models import fetch_database
from systemtest.utils.utils import dict_counter

@app.task()
def sync_database() -> dict[str, int]:
    quality_system = quality_models.QualitySystem.objects
    count_dict = {}

    query = Q(operation_status="W")
    waiting_systems = quality_system.filter(query).values("workunit")

    for row in fetch_database():
        try:
            quality_system.update_or_create(**row)
        except IntegrityError:
            dict_counter(count_dict, "EXISTING")

        waiting_systems = waiting_systems.exclude(workunit=row.get("workunit"))
        dict_counter(count_dict, "FETCH")

    for workunit in waiting_systems:
        system = quality_system.get(**workunit)
        system.operation_status = "A"
        system.save()

    count_dict["REMOVED"] = len(waiting_systems)
    return count_dict
