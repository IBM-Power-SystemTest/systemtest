from django import forms
from systemtest.quality import models

class QualitySystemForm(forms.ModelForm):
    class Meta:
        model = models.QualitySystem
        fields = (
            "quality_status",
            "comment"
        )
