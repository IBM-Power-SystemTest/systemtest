# Django filters
import django_filters as filters

# Django db
from django.db.models import Q

# APPs
from systemtest.utils.models import get_objects_by_query
from systemtest.pts import models as pts_models, forms as pts_forms


class RequestFilterSet(filters.FilterSet):
    query = Q(name="CLOSE GOOD") | Q(name="CLOSE BAD") | Q(name="CANCEL")
    status = get_objects_by_query(pts_models.RequestStatus, query)

    request_status = filters.ModelChoiceFilter(queryset=status)
    modified = filters.DateRangeFilter()

    class Meta:
        model = pts_models.Request
        fields = (
            "id",
            "request_status",
            "part_number",
            "serial_number",
            "request_group__request_group_workspace",
            "request_group__system_number",
            "request_group__is_vpd",
            "request_group__is_loaner",
            "ncm_tag",
            "modified",
        )


class HistoryFilterSet(filters.FilterSet):
    created = filters.DateRangeFilter()

    class Meta:
        model = pts_models.RequestHistory
        fields = (
            "request__id",
            "request_status",
            "part_number",
            "serial_number",
            "request__request_group__request_group_workspace",
            "request__request_group__system_number",
            "request__request_group__is_vpd",
            "request__request_group__is_loaner",
            "request__ncm_tag",
            "created",
        )
