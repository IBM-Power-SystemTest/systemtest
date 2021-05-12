# Django
from django import forms

# APPS
from systemtest.pts import models
from systemtest.pts.forms import RequestPartForm
from systemtest.utils.forms import set_placeholder


class RequestUpdateListForm(forms.ModelForm, RequestPartForm):
    """
    Django Form for update a request, mainly part number, serial number, and status
        References:
            https://docs.djangoproject.com/en/3.1/topics/forms/
            https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/

            https://docs.djangoproject.com/en/3.1/ref/forms/api/
            https://docs.djangoproject.com/en/3.1/ref/forms/fields/

    Attributes:
        part_id:
            Field to input the part number and serial number making
            validations and filtering input ( from RequestPartForm )
        request_status:
            Requirement status, combobox with status as choices filter
            choices in the view ( or when the form is instantiated )
        comment:
            Addition comment
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
            None, creates an intance, remove field placeholder
        """

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

# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/
# https://docs.djangoproject.com/en/3.1/ref/forms/models/
RequestFormset = forms.modelformset_factory(
    models.Request,
    RequestUpdateListForm,
    extra=0,
)


class RequestReturnListForm(RequestUpdateListForm):
    """
    Django Form for update requests in pending and return
        References:
            https://docs.djangoproject.com/en/3.1/topics/forms/
            https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/

            https://docs.djangoproject.com/en/3.1/ref/forms/api/
            https://docs.djangoproject.com/en/3.1/ref/forms/fields/

    Attributes:
        Meta:
            Override ModelForm options, adds new field (ncm_tag)
    """

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

# https://docs.djangoproject.com/en/3.1/topics/forms/formsets/
# https://docs.djangoproject.com/en/3.1/ref/forms/models/
ReturnFormset = forms.modelformset_factory(
    models.Request,
    RequestReturnListForm,
    extra=0
)
