# Python
from typing import Any, Dict

# Django
from django import forms

# APPs
from systemtest.pts import models
from systemtest.utils.forms import set_placeholder


class RequestGroupForm(forms.ModelForm):
    """
    Django ModelForm for RequestGroup
        References:
            https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
            https://docs.djangoproject.com/en/3.1/ref/forms/fields/
            https://docs.djangoproject.com/en/3.1/topics/forms/
            https://docs.djangoproject.com/en/3.1/ref/forms/api/

    Attributes:
        system_number:
            Or MFGN
        system_cell:
            Logic testcell where the system is
        request_group_workspace:
            Location where the system is
        request_bay:
            Cluster of user
        part_description:
            Name or description of part to request
        is_loaner:
            Only if the system needs loaner parts
        is_vpd:
            Parts that are given to change
        is_serialized:
            If Part number has serial number
        qty:
            Number of pieces of the same PN
        Meta:
            ModelForm Options
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

        # Saving each field into var for future short sintax
        system_number = self.fields["system_number"]
        system_cell = self.fields["system_cell"]
        request_bay = self.fields["request_bay"]
        part_description = self.fields["part_description"]

        # Adding placeholder attribute to fields
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

    def clean_qty(self) -> int:
        """
        Form valiation for 'qty' field, make sure this is not greater
        than 10 nor less than 1
            References:
                https://docs.djangoproject.com/en/3.1/ref/forms/validation/#cleaning-a-specific-field-attribute

        Args:
            self:
                Instance form

        Returns:
            If the field comply the requirements, it returns its value
            In this case a number from 1 to 10
        """

        qty = self.cleaned_data['qty']
        if qty < 1:
            raise forms.ValidationError("The minimum requirement is '1'")
        elif qty > 10:
            raise forms.ValidationError("The maximum requirement is '10'")
        return qty

    def clean(self) -> Dict[str, Any]:
        """
        Form valiation for all fields
            References:
                https://docs.djangoproject.com/en/3.1/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other

        Args:
            self:
                Instance form

        Returns:
            If the fields comply the requirements, it returns its data
        """

        data = super().clean()
        if data.get("is_vpd") and data.get("qty") > 1:
            raise forms.ValidationError(
                "It is not possible to request more than one VPD"
            )

        if data.get("is_vpd") and not data.get("is_serialized"):
            raise forms.ValidationError("All VPDs are serialized")

        return data
