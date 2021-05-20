# Django
from django import forms
from django.db import models
from django.forms.models import modelformset_factory

# Django filters
import django_filters as filters

# APPs
from systemtest.people import models as people_models
from systemtest.utils.forms import DateInput, CharInFilter
from systemtest.people.utils.models import get_users_leads


class PeopleRequirementForm(forms.ModelForm):
    for_user = forms.ModelChoiceField(
        help_text="User who receives the request",
        queryset=get_users_leads()
    )

    class Meta:
        model = people_models.PeopleRequirement
        fields = (
            "type",
            "for_user",
            "start",
            "days",
            "description",
        )

        widgets = {"start": DateInput}


class PeopleRequirementUpdateForm(forms.ModelForm):

    status = forms.ModelChoiceField(
        queryset=people_models.PeopleStatus.objects.exclude(name="CANCEL")
    )

    class Meta:
        model = people_models.PeopleRequirement
        fields = (
            "status",
            "comment",
            "start",
            "days"
        )
        widgets = {"start": DateInput}


# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/
# https://docs.djangoproject.com/en/3.1/ref/forms/models/
RequirementFormset = modelformset_factory(
    people_models.PeopleRequirement,
    form=PeopleRequirementUpdateForm,
    extra=0
)


class PeopleHistoryFilterSet(filters.FilterSet):
    requirement__id = CharInFilter()
    requirement__by_user = CharInFilter()
    requirement__for_user = CharInFilter()
    days = CharInFilter()
    start = filters.DateRangeFilter()
    created = filters.DateRangeFilter()

    class Meta:
        model = people_models.PeopleHistory
        fields = (
            "requirement__id",
            "status",
            "start",
            "days",
            "requirement__by_user",
            "requirement__for_user",
            "created",
            "requirement__description",
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
