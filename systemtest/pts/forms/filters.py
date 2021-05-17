# Django filters
import django_filters as filters

# Django
from django.db.models import Q
from django import forms
from django.db import models

# APPs
from systemtest.utils.models import get_objects_by_query
from systemtest.utils.forms import NumberInFilter, CharInFilter
from systemtest.pts import models as pts_models, forms as pts_forms


class RequestFilterSet(filters.FilterSet):
    query = Q(name="CLOSE GOOD") | Q(name="CLOSE BAD") | Q(name="CANCEL")
    status = get_objects_by_query(pts_models.RequestStatus, query)

    id = NumberInFilter()
    request_status = filters.ModelChoiceFilter(queryset=status)
    ncm_tag = NumberInFilter()
    part_number = CharInFilter()
    serial_number = CharInFilter()
    request_group__system_number = CharInFilter()
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

        filter_overrides = {
            models.CharField: {
                "filter_class": filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
            models.BooleanField: {
                "filter_class": filters.BooleanFilter,
                "extra": lambda f: {
                    "widget": forms.CheckboxInput,
                },
            }
        }


class HistoryFilterSet(filters.FilterSet):
    request__id = NumberInFilter()
    part_number = CharInFilter()
    serial_number = CharInFilter()
    request__request_group__system_number = CharInFilter()
    request__ncm_tag = NumberInFilter()
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

        filter_overrides = {
            models.CharField: {
                "filter_class": filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
            models.BooleanField: {
                "filter_class": filters.BooleanFilter,
                "extra": lambda f: {
                    "widget": forms.CheckboxInput,
                },
            }
        }
