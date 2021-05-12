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
from systemtest.pts.utils.models import get_status


class TransitRequestView(BaseRequestListView):
    """
    RequestListView for Request in transit
    """

    template_name = "pts/transit.html"
    success_url = reverse_lazy("pts:transit")

    query = Q(request_status__name="TRANSIT")
    next_status_query = Q(name="PENDING")

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_template_names(self) -> list[str]:
        """
        Depends of the groups user can see one view/template or other

        Args:
            self:
                Instance

        Returns:
            Changes the attribute template_name and
            after execute the orinal method
        """

        if self.user_groups.filter(name="TA"):
            self.template_name = "pts/transit_ta.html"

        if self.user_groups.filter(name="IPIC"):
            self.template_name = "pts/transit_ipic.html"
            self.validate_serial = False
            self.next_status = Q(name="TRANSIT")
        return super().get_template_names()

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        if self.user_groups.filter(name="IPIC"):
            return True
        return super().is_valid_serial(request, serial)

    def get_new_status(self, request: Type[pts_models.Request]):
        """
        Executes a query to get status to move the Model in case
        everything has gone well

        Args:
            self:
                Instance

        Returns:
            If user is in 'IPIC' group hold status on 'TRANSIT',
            if request is a VPD or TPM move status until 'CLOSE GOOD',
            Otherwise, continue with normal method
        """

        if request.request_group.is_vpd:
            return self.status_model.objects.get(name="CLOSE GOOD")
        if self.user_groups.filter(name="IPIC"):
            return self.status_model.objects.get(name="TRANSIT")
        return super().get_new_status(request)


class ReturnToOpen(DeleteView):
    model = pts_models.Request
    success_url = reverse_lazy("pts:transit")

    def get(self, *args, **kwargs) -> HttpResponse:
        """
        Redirect Http GET to delete method

        Args:
            args:
                Positional arguments
            kwargs:
                Keyword arguments

        Returns:
            Httpresponse to delete method
        """

        return self.delete()

    def delete(self) -> HttpResponse:
        """
        Change the status of object on the fetched object and then redirect to the
        success URL.

        Args:
            self:
                Instance

        Returns:
            Redirect to succes url
        """

        self.object = self.get_object()

        self.object.request_status = get_status("OPEN")
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
