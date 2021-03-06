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

class TransitRequestView(BaseRequestListView):
    template_name = "pts/transit.html"
    success_url = reverse_lazy("pts:transit")

    query = Q(request_status__name="TRANSIT")
    next_status_query = Q(name="PENDING")

    def get_template_names(self) -> list[str]:
        self.user_groups = self.request.user.groups.all()
        if self.user_groups.filter(name="TA"):
            self.template_name = "pts/transit_ta.html"

        if self.user_groups.filter(name="IPIC"):
            self.template_name = "pts/transit_ipic.html"
            self.validate_serial = False
            self.next_status = Q(name="TRANSIT")
        return super().get_template_names()

    def get_new_status(self, request: Type[pts_models.Request]):
        if request.request_group.is_vpd:
            return self.status_model.objects.get(name="CLOSE GOOD")
        if self.user_groups.filter(name="IPIC"):
            return self.status_model.objects.get(name="TRANSIT")
        return super().get_new_status(request)

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        self.user_groups = self.request.user.groups.all()
        if self.user_groups.filter(name="IPIC"):
            return True
        return super().is_valid_serial(request, serial)


class RequestReopen(DeleteView):
    model = pts_models.Request
    success_url = reverse_lazy("pts:transit")
    template_name = "pts/request_cancel.html"

    def get(self, request, *args, **kwargs):
        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="IPIC"):
            return self.delete()

    def delete(self) -> HttpResponse:
        """
        Change the status of object on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        self.object.request_status = pts_models.RequestStatus.objects.get(name="OPEN")
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
