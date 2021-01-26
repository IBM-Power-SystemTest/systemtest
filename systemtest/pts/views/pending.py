# Django Views
from typing import Type
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

# Django HTTP
from django.urls.base import reverse_lazy

# Django db
from django.db.models import Q

# APPS
from systemtest.pts import models as pts_models, forms as pts_forms
from .views import BaseRequestListView

# class PendingPartListView(ListView):
#     template_name = "pts/pending.html"
#     queryset = pts_models.Request.objects.filter(request_status__name="PENDING")

#     def get_template_names(self) -> list[str]:
#         user_groups = self.request.user.groups.all()
#         if user_groups.filter(name="TA"):
#             self.template_name = "pts/pending_ta.html"

#         return super().get_template_names()


class PendingPartListView(BaseRequestListView):
    template_name = "pts/pending.html"
    success_url = reverse_lazy("pts:pending")

    query = Q(request_status__name="PENDING")
    next_status_query = Q(name="RETURN")

    choice_query = Q(pk__gte=7) & Q(pk__lte=10) | Q(name="PENDING")

    def get_template_names(self) -> list[str]:
        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="TA"):
            self.template_name = "pts/pending_ta.html"

        return super().get_template_names()

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        if serial != request.serial_number:
            return True
        return False

class UpdatePendingRequestView(UpdateView):
    model = pts_models.Request
    template_name = "pts/return_detail.html"
    form_class = pts_forms.ReturnRequestForm
