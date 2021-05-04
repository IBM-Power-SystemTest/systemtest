from django import forms

from systemtest.pts import models
from systemtest.utils.forms import set_placeholder

from systemtest.pts.forms import RequestPartForm

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
