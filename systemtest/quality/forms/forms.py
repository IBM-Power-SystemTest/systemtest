# Django
from django.db import models
from django import forms
from django.forms.models import modelformset_factory

# Django filters
import django_filters as filters

# APPs
from systemtest.quality import models as quality_models

# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/
# https://docs.djangoproject.com/en/3.1/ref/forms/models/
QualitySystemFormset = modelformset_factory(
    quality_models.QualitySystem,
    fields=["quality_status", "comment"],
    extra=0
)


class SystemHistoryFilterSet(filters.FilterSet):
    created = filters.DateRangeFilter()
    operation_status = filters.ChoiceFilter(choices=(("A", "A"), ("W", "W")))

    class Meta:
        model = quality_models.QualityHistory
        fields = (
            "system__workunit",
            "system__system_number",
            "operation_number",
            "operation_status",
            "quality_status",
            "system__product_line",
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
