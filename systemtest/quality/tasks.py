# Python
from typing import Any

# Django
from django.conf import Settings, settings

# Celery
from config.celery_app import app

# APPs
from systemtest.utils.db2 import Database
from systemtest.quality import forms as quality_forms, models as quality_models

database = Database(**settings.DATABASES.get("db2"))


def fetch_database() -> dict[str, Any]:
    sql = database.get_sql(settings.QUALITY_SQL_PATH)
    required_columns = {
        "SYSTEM_NUMBER",
        "WORKUNIT",
        "OPERATION_STATUS"
    }
    optional_columns = {
        "WORKUNIT_QTY",
        "PRODUCT_LINE",
        "OPERATION_NUMBER"
    }

    for row in database.fetch(sql):
        columns = set(row.keys())
        if (required_columns - columns):
            continue

        data = {column.lower(): row.get(column)
                for column in (required_columns | optional_columns)}
        yield data


@app.task()
def sync_database():
    quality_system = quality_models.QualitySystem.objects
    waiting_systems = quality_system.filter(operation_status="W")
    workunit_set = waiting_systems.values("workunit")

    for row in fetch_database():
        quality_system.update_or_create(**row)
        workunit_set = workunit_set.exclude(workunit=row.get("workunit"))

    for workunit in workunit_set:
        system = quality_system.get(**workunit)
        system.operation_status = "A"
        system.save()
