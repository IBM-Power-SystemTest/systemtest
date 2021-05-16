# Django
from django.forms.models import modelformset_factory

# Django filters
import django_filters as filters

# APPs
from systemtest.quality import models

# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/
# https://docs.djangoproject.com/en/3.1/ref/forms/models/
QualitySystemFormset = modelformset_factory(
    models.QualitySystem,
    fields=["quality_status", "comment"],
    extra=0
)


class SystemHistoryFilterSet(filters.FilterSet):
    created = filters.DateRangeFilter()

    class Meta:
        model = models.QualityHistory
        fields = (
            "system__workunit",
            "system__system_number",
            "operation_number",
            "operation_status",
            "quality_status",
            "system__product_line",
            "created",
        )
