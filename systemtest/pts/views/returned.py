# Python
from typing import Any, Type
from django.forms.models import model_to_dict

# Django HTTP
from django.urls.base import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http.response import HttpResponse, HttpResponseRedirect

# Django db
from django.db.models import Q

# APP PTS
from systemtest.pts import models as pts_models, forms as pts_forms
from systemtest.pts.utils.models import get_status
from .views import BaseRequestListView


class ReturnPartListView(BaseRequestListView):
    """
    RequestListView for Request returned as GOOD or BAD
    """

    template_name = "pts/return.html"
    success_url = reverse_lazy("pts:return")

    form_class = pts_forms.ReturnFormset

    query = (
        Q(request_status__name="GOOD") |
        Q(request_status__name="BAD")
    )

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

        if self.user_groups.filter(name="IPIC"):
            self.template_name = "pts/return_ipic.html"

        elif self.user_groups.filter(name="IPIC NCM"):
            self.template_name = "pts/return_ipic_ncm.html"

        elif self.user_groups.filter(name="TA"):
            self.template_name = "pts/return_ta.html"
            self.validate_serial = False
        return super().get_template_names()

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        """
        Rules to verify serial number, If the user has the 'TA' group
        it does not validate the serial, otherwise, the serial has to be same

        Args:
            request:
                Request object to get the original serial number
            serial:
                New serial number to compare with request serial number

        Returns:
            Boolean depends of the validation case
        """

        if self.user_groups.filter(name="TA"):
            return True
        return super().is_valid_serial(request, serial)

    def get_new_status(self, request: Type[pts_models.Request]) -> Any:
        """
        Next status depends of the current status so, validates options

        Args:
            request:
                Request object to get current status
        Returns:
            Execute original method after change the
            next_status or next_status_query
        """

        status = str(request.request_status)
        if self.user_groups.filter(name="TA"):
            self.next_status = request.request_status
        if status == "BAD":
            self.next_status_query = Q(name="CLOSE BAD")
        elif status == "GOOD":
            self.next_status_query = Q(name="CLOSE GOOD")

        return super().get_new_status(request)


class ReturnToPending(DeleteView):
    model = pts_models.Request
    success_url = reverse_lazy("pts:return")

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

        self.object.request_status = get_status("PENDING")
        self.object.ncm_tag = None
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
