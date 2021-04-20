from django.forms.models import modelformset_factory

from systemtest.quality import models


QualitySystemFormset = modelformset_factory(
    models.QualitySystem,
    fields=["quality_status", "comment"],
    extra=0
)
