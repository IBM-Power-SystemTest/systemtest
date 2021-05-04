import re

from django import forms

from systemtest.utils.forms import set_placeholder


class RequestPartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        part_id = self.fields["part_id"]
        set_placeholder(part_id, "eg. 78P4198 YH10MS0C3090")

    part_id = forms.CharField(
        label="Part Number [ PN + SN ]",
        help_text="""
            [ 11S ]
            [ P78P4198 SYH10MS0C3090 ]
            [ 78P4198 YH10MS0C3090 ]
            [ 78P4198YH10MS0C3090 ]
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
