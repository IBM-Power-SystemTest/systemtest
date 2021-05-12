# Django
from django import forms
from django.forms.models import modelformset_factory

# APPs
from systemtest.quality import models

# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/
# https://docs.djangoproject.com/en/3.1/ref/forms/models/
QualitySystemFormset = modelformset_factory(
    models.QualitySystem,
    fields=["quality_status", "comment"],
    extra=0
)
