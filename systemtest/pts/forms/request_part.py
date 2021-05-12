# Python
import re

# Django
from django import forms

# APPs
from systemtest.utils.forms import set_placeholder


class RequestPartForm(forms.Form):
    """
    Django Form for get part_number and serial_number in one field
        References:
            https://docs.djangoproject.com/en/3.1/topics/forms/
            https://docs.djangoproject.com/en/3.1/ref/forms/api/
            https://docs.djangoproject.com/en/3.1/ref/forms/fields/

    Attributes:
        part_id:
            Field to input the part number and serial number making
            validations and filtering input
    """

    def __init__(self, *args, **kwargs):
        """
        Customizing the form when initialized, like remove suffix and
        modify fields

        Args:
            args:
                Positional args for ModelForm
            kwargs:
                Keyword args for ModelForm

        Returns:
            None, creates an intance, remove labe_sufix and adds
            placeholder to some fields
        """

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
        """
        Form valiation for 'part_id' field, validate regex pattern
            References:
                https://docs.djangoproject.com/en/3.1/ref/forms/validation/#cleaning-a-specific-field-attribute

        Args:
            self:
                Instance form

        Returns:
            Validate part_id and get the relevant information from the
            field assign it to a new key of the data (pn and sn)
        """

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
    """
    Django BaseFormSet to creates several RequestPartForm to creates a new
    requirement of parts, being complementary to RequestGroupForm
        References:
            https://docs.djangoproject.com/en/3.1/topics/forms/formsets/
    """

    def clean(self):
        """

        """
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        # Gets all part ids from multiple forms (With only one field)
        part_id_set = self.cleaned_data

        # Save only unique part number, and remove None as part number
        part_number_set = {
            part_id.get("pn") for part_id in part_id_set
        } - {None}

        # If does not have a single valid part number . . .
        if not part_number_set:
            error_message = "You must enter at least a valid part number"
            raise forms.ValidationError(error_message)

        # If has more than one part number . . .
        if len(part_number_set) > 1:
            error_message = "Different part numbers are being required {} ".format(
                ", ".join(part_number_set)
            )
            raise forms.ValidationError(error_message)

        # Save all serial numbers here
        serial_number_list = []

        # If exists the same serial number in the formset save here
        serial_duplicate_set = set()

        for part_id in part_id_set:

            # Checking if serial number is not already in the serial number list
            # If found a same serial add to serial_duplicate_set and continue
            if (sn := part_id.get("sn")) in serial_number_list:
                serial_duplicate_set.add(sn)
            serial_number_list.append(sn)

        # If repeated serials were found
        if serial_duplicate_set:
            error_message = "The same serial is required {} ".format(
                ", ".join(serial_duplicate_set)
            )
            raise forms.ValidationError(error_message)
