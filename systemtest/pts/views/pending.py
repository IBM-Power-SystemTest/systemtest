# Django Views
from typing import Type

# Django Forms
from django.forms.models import BaseModelForm

# Django Views
from django.views.generic.edit import UpdateView

# Django HTTP
from django.urls.base import reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect

# Django db
from django.db.models import Q

# APPS
from systemtest.pts import models as pts_models, forms as pts_forms
from .views import BaseRequestListView


class PendingPartListView(BaseRequestListView):
    template_name = "pts/pending.html"
    success_url = reverse_lazy("pts:pending")

    query = (
        Q(request_status__name="PENDING") |
        Q(request_status__name="INSTALADO EN OTRA WU") |
        Q(request_status__name="REVISION CON EL ME")
    )
    next_status_query = Q(name="GOOD")

    choice_query = (
        Q(name="INSTALADO EN OTRA WU") |
        Q(name="REVISION CON EL ME")
    )

    form_class = pts_forms.ReturnFormset

    def get_template_names(self) -> list[str]:
        if self.user_groups.filter(name="TA"):
            self.template_name = "pts/pending_ta.html"

        return super().get_template_names()

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        if serial != request.serial_number:
            return True
        return False

    def form_valid(self, forms: list[BaseModelForm]) -> HttpResponse:
        for form in forms:
            data = form.cleaned_data
            if not data.get("part_id"):
                continue

            request = form.save(commit=False)

            request.part_number = data.get("pn")
            if sn := data.get("sn"):
                request.serial_number = sn

            if new_status := data.get("request_status"):
                self.next_status = new_status

            if ncm_tag := data.get("ncm_tag"):
                request.ncm_tag = ncm_tag
                self.next_status = None
                self.next_status_query = Q(name="BAD")

            request.request_status = self.get_new_status(request)
            request.save()

        return HttpResponseRedirect(self.get_success_url())
