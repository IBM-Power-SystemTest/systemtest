import re
from typing import Any, Dict

from django import forms

from systemtest.pts import models


class RequestGroupForm(forms.ModelForm):
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
                attrs={"onchange": "this.form.submit()"}
            )
        }

    def clean(self) -> Dict[str, Any]:
        data = super().clean()
        if data.get("is_vpd") and data.get("qty") > 1:
            raise forms.ValidationError("No es posible pedir mas de una VPD")

        if data.get("is_vpd") and not data.get("is_serialized"):
            raise forms.ValidationError("Todas las VPD son serializadas")

        return data


class RequestPartForm(forms.Form):
    part_id = forms.CharField(
        max_length=30,
        min_length=7,
        strip=True,
        required=False,
    )

    def clean_part_id(self):
        data = self.cleaned_data["part_id"]

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
