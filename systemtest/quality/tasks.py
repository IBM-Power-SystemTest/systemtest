# Django
from django.conf import Settings, settings

# Celery
from config.celery_app import app

# APPs
from systemtest.utils.db2 import Database
from systemtest.quality import forms as quality_forms, models as quality_models

database = Database(**settings.DATABASES.get("db2"))

@app.task(name="quality.fetch_database")
def fetch_database(name="quality.fetch_databases") -> None:
    sql = database.get_sql(settings.QUALITY_SQL_PATH)
    quality_system = quality_models.QualitySystem

    required_columns = {
        "SYSTEM_NUMBER",
        "WORKUNIT",
        "OPERATION_STATUS"
    }
    optional_columns = {
        "WORKUNIT_QTY",
        "PRODUCT_LINE",
        "MACHINE_TYPE",
        "SYSTEM_MODEL",
        "OPERATION_NUMBER"
    }

    for row in database.fetch(sql):
        columns = set(row.keys())
        if (required_columns - columns):
            continue

        data = {column.lower(): row.get(column)
                for column in (required_columns | optional_columns)}

        quality_system.objects.update_or_create(**data)
