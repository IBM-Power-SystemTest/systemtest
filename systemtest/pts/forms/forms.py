import re
from typing import Any, Dict

from django import forms

from systemtest.pts import models
from systemtest.utils.forms import set_placeholder


class RequestGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        system_number = self.fields["system_number"]
        system_cell = self.fields["system_cell"]
        request_group_workspace = self.fields["request_group_workspace"]
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
            raise forms.ValidationError("El minimo de requerimientos es '1'")
        elif qty > 10:
            raise forms.ValidationError("El maximo de requerimientos es '10'")
        return qty

    def clean(self) -> Dict[str, Any]:
        data = super().clean()
        if data.get("is_vpd") and data.get("qty") > 1:
            raise forms.ValidationError("No es posible pedir mas de una VPD")

        if data.get("is_vpd") and not data.get("is_serialized"):
            raise forms.ValidationError("Todas las VPD son serializadas")

        return data


class RequestPartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = "78P4198 YH10MS0C3090"

    part_id = forms.CharField(
        label="11S",
        help_text="PN + SN",
        max_length=30,
        min_length=7,
        strip=True,
        required=False,
    )

    def clean_part_id(self):
        data = self.cleaned_data["part_id"]
        if not data:
            return None

        prefix_pattern = r"^\s*(11[sS])?"
        pn_pattern = r"[pP]?(?P<pn>[0-9a-zA-Z]{7})"
        sn_pattern = r"[sS]?(?P<sn>[0-9a-zA-Z]{12})?"

        pattern = (
            prefix_pattern +
            r"\s*" +
            pn_pattern +
            r"\s*" +
            sn_pattern +
            r"\s*$"
        )
        part_id_regex = re.compile(pattern)

        if not (match := part_id_regex.fullmatch(data)):
            error_message = "11S no es valido, sin match para el PN o SN"
            raise forms.ValidationError(error_message)

        groups_matched = match.groupdict()
        self.cleaned_data["sn"] = groups_matched.get("sn")
        self.cleaned_data["pn"] = groups_matched.get("pn")

        return data


class RequestUpdateListForm(forms.ModelForm, RequestPartForm):
    comment = forms.CharField(
        max_length=30,
        strip=True,
        required=False,
    )
    part_id = forms.CharField(
        max_length=30,
        min_length=7,
        strip=True,
        required=False,
    )

    class Meta:
        model = models.Request
        fields = (
            "comment",
            "part_id",
            "request_status"
        )


RequestFormset = forms.modelformset_factory(
    models.Request,
    RequestUpdateListForm,
    extra=0,
)


class RequestReturnListForm(RequestUpdateListForm):
    class Meta:
        model = models.Request
        fields = (
            "comment",
            "part_id",
            "request_status",
            "ncm_tag",
        )


ReturnFormset = forms.modelformset_factory(
    models.Request,
    RequestReturnListForm,
    extra=0
)
