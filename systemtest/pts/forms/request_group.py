from typing import Any, Dict

from django import forms

from systemtest.pts import models
from systemtest.utils.forms import set_placeholder


class RequestGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        system_number = self.fields["system_number"]
        system_cell = self.fields["system_cell"]
        request_bay = self.fields["request_bay"]
        part_description = self.fields["part_description"]

        system_number = set_placeholder(system_number, "eg. 1AU80N8")
        system_cell = set_placeholder(system_cell, "eg. C153")
        request_bay = set_placeholder(request_bay, "eg. Z100")
        part_description = set_placeholder(part_description, "eg. DIMM")

    class Meta:
        model = models.RequestGroup
        fields = (
            "system_number",
            "system_cell",
            "request_group_workspace",
            "request_bay",
            "part_description",
            "is_loaner",
            "is_vpd",
            "is_serialized",
            "qty",
        )

        widgets = {
            "qty": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 10,
                    "onchange": "this.form.submit()"
                }
            )
        }

    def clean_qty(self):
        qty = self.cleaned_data['qty']
        if qty < 1:
            raise forms.ValidationError("The minimum requirement is '1'")
        elif qty > 10:
            raise forms.ValidationError("The maximum requirement is '10'")
        return qty

    def clean(self) -> Dict[str, Any]:
        data = super().clean()
        if data.get("is_vpd") and data.get("qty") > 1:
            raise forms.ValidationError(
                "It is not possible to request more than one VPD")

        if data.get("is_vpd") and not data.get("is_serialized"):
            raise forms.ValidationError("All VPDs are serialized")

        return data
