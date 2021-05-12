

# Django
from django.conf import Settings, settings

# APPs
from systemtest.quality import forms as quality_forms, models as quality_models
from systemtest.utils.db2 import Database



def get_quality_status(status_name: str) -> quality_models.QualityStatus:
    """
    Gets a specific QualityStatus by exact name

    Args:
        status_name:
            Name of status to fetch

    Raises:
        DoesNotExist:
            QualityStatus matching query does not exist

    Returns:
        QualityStatus object
    """
    return quality_models.QualityStatus.objects.get(name=status_name)

def fetch_database() -> dict:
    database = Database(**settings.DATABASES.get("db2"))

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
