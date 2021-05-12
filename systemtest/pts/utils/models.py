# Django
from django.db.models.query import QuerySet

# APPs
from systemtest.pts import models as pts_models
from systemtest.utils.db2 import Database


def get_request_by_status_name(status_name: str) -> QuerySet[pts_models.Request]:
    """
    Django QuerySet with all Request objects/rows in a specific status

    Args:
        status_name:
            Name of status to fetch

    Returns:
        Django QuerySet of Request objects/rows
    """
    return pts_models.Request.objects.filter(request_status__name=status_name)


def get_status(status_name: str) -> pts_models.RequestStatus:
    """
    Gets a specific RequestStatus by exact name

    Args:
        status_name:
            Name of status to fetch

    Raises:
        DoesNotExist:
            RequestStatus matching query does not exist

    Returns:
        RequestStatus object
    """
    return pts_models.RequestStatus.objects.get(name=status_name)


def get_ncm(request: pts_models.Request, database: Database) -> dict:
    """
    Performs query to DB2 and get NCM data as tag and part location

    Args:
        request:
            Request object to fetch NCM data.
        database:
            Database instance to execute query

    Returns:
        Dictionary with NCM data if it exits and additional flag for
        location part or an empty dictionary in case of not finding ncm
    """

    # Create a dict with data for execute query
    data = {
        "part_number": request.part_number,
        "serial_number": request.serial_number,
        "created": request.created
    }

    # Add dinamic data to SQL query
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

    rows = database.fetch(sql, False)

    # Get first row from query if no row gets empty dict
    row = next(rows, {})

    # If row has column 'NCM_TAG' named in the query above
    if ncm_tag := row.get("NCM_TAG"):
        data["ncm_tag"] = ncm_tag

        # Fetch next row if exists to validate the location of part
        row = next(rows, {})
        data["is_returned"] = row.get("CURRENT_LOCATION", "").strip() == "PNCM"

        return data

    # If any ncm_data was found return empty dict
    return {}
