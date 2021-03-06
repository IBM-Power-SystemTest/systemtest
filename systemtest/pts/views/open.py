# Python
from typing import Type

# Django HTTP
from django.urls.base import reverse_lazy
from django.http.response import HttpResponseRedirect, HttpResponse

# Django db
from django.db.models import Q

# Django Views
from django.views.generic.edit import DeleteView

# APP PTS
from .views import BaseRequestListView
from systemtest.pts import models as pts_models


class OpenRequestView(BaseRequestListView):
    template_name = "pts/open.html"
    success_url = reverse_lazy("pts:open")

    query = (
        Q(request_status__pk=1) |
        Q(request_status__pk__gte=12)
    )

    choice_query = Q(pk=1) | Q(pk__gte=12)

    next_status_query = Q(name="TRANSIT")

    def get_template_names(self) -> list[str]:
        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="IPIC"):
            self.template_name = "pts/open_ipic.html"
        elif user_groups.filter(name="TA"):
            self.template_name = "pts/open_ta.html"

        return super().get_template_names()

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        if serial != request.serial_number:
            return True
        return False


class RequestCancel(DeleteView):
    model = pts_models.Request
    success_url = reverse_lazy("pts:open")
    template_name = "pts/request_cancel.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return HttpResponseRedirect(self.get_success_url())
        return self.delete()

    def delete(self) -> HttpResponse:
        """
        Change the status of object on the fetched object and then redirect to the
        success URL.
        """
        self.object.request_status = pts_models.RequestStatus.objects.get(name="CANCEL")
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
