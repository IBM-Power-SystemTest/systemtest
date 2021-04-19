import re
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


class RequestPartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        part_id = self.fields["part_id"]
        set_placeholder(part_id, "eg. 78P4198 YH10MS0C3090")

    part_id = forms.CharField(
        label="Part Number [ + Serial Number ]",
        help_text="""
            Some valid formats:
            11S78P4198YH10MS0C3090
            P78P4198 SYH10MS0C3090
            78P4198 YH10MS0C3090
            78P4198YH10MS0C3090
            """,
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
            error_message = "11S is not valid, check the valid formats"
            raise forms.ValidationError(error_message)

        groups_matched = match.groupdict()
        self.cleaned_data["sn"] = groups_matched.get("sn")
        self.cleaned_data["pn"] = groups_matched.get("pn")

        return data


class RequestPartFormset(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        part_id_set = self.cleaned_data
        part_number_set = {
            part_id.get("pn") for part_id in part_id_set
        } - {None}

        if not part_number_set:
            error_message = "You must enter at least a valid part number"
            raise forms.ValidationError(error_message)

        if len(part_number_set) > 1:
            error_message = "Different part numbers are being required {} ".format(
                ", ".join(part_number_set)
            )
            raise forms.ValidationError(error_message)

        serial_number_list = []
        serial_duplicate_set = set()
        for part_id in part_id_set:
            if (sn := part_id.get("sn")) in serial_number_list:
                serial_duplicate_set.add(sn)
            serial_number_list.append(sn)

        if serial_duplicate_set:
            error_message = "The same serial is required {} ".format(
                ", ".join(serial_duplicate_set)
            )
            raise forms.ValidationError(error_message)


class RequestUpdateListForm(forms.ModelForm, RequestPartForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        part_id = self.fields["part_id"]
        set_placeholder(part_id, "")

    comment = forms.CharField(
        max_length=30,
        strip=True,
        required=False,
    )
    part_id = forms.CharField(
        help_text="""
            Some valid formats:
            11S78P4198YH10MS0C3090
            P78P4198 SYH10MS0C3090
            78P4198 YH10MS0C3090
            78P4198YH10MS0C3090
            """,
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
        widgets = {
            "ncm_tag": forms.TextInput()
        }


ReturnFormset = forms.modelformset_factory(
    models.Request,
    RequestReturnListForm,
    extra=0
)
