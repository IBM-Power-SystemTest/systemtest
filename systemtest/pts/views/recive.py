# Django Views
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

# APPS
from systemtest.pts import models as pts_models, forms as pts_forms


class RecivePartListView(ListView):
    template_name = "pts/recive.html"
    queryset = pts_models.Request.objects.filter(request_status__name="RECIVE")

    def get_template_names(self) -> list[str]:
        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="TA"):
            self.template_name = "pts/recive_ta.html"

        return super().get_template_names()

class UpdateRequestView(UpdateView):
    model = pts_models.Request
    template_name = "pts/return_detail.html"
    form_class = pts_forms.ReturnRequestForm
