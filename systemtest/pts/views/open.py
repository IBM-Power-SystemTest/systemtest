# Python
from typing import Type

# Django HTTP
from django.urls.base import reverse_lazy
from django.http.response import HttpResponseRedirect, HttpResponse

# Django db
from django.db.models import Q

# Django Views
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# APP PTS
from systemtest.pts import models as pts_models, views as pts_views
from systemtest.pts.utils.models import get_status


class OpenRequestView(pts_views.BaseRequestListView):
    """
    RequestListView for Request in 'OPEN' status
    """

    template_name = "pts/open.html"
    success_url = reverse_lazy("pts:open")

    query = (
        Q(request_status__pk=1) |
        Q(request_status__pk__gte=12)
    )

    choice_query = Q(pk=1) | Q(pk__gte=12)

    next_status_query = Q(name="TRANSIT")

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

        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="IPIC"):
            self.template_name = "pts/open_ipic.html"
        elif user_groups.filter(name="TA"):
            self.template_name = "pts/open_ta.html"

        return super().get_template_names()

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        """
        Rules to verify serial number, If the user has the 'TA' group
        it does not validate the serial, otherwise, the serial has to be different

        Args:
            request:
                Request object to get the original serial number
            serial:
                New serial number to compare with request serial number

        Returns:
            Boolean depends of the validation case
        """

        if serial != request.get_first_request().serial_number or self.user_groups.filter(name="TA"):
            return True
        return False

    def get_new_status(self, request: Type[pts_models.Request]):
        """
        Executes a query to get status to move the Model in case
        everything has gone well

        Args:
            self:
                Instance

        Returns:
            If user has not 'TA' group foward to next status
            if user is in 'TA' group hold status on 'OPEN'
        """

        if self.user_groups.filter(name="TA"):
            return self.status_model.objects.get(name="OPEN")
        return super().get_new_status(request)


class RequestCancel(LoginRequiredMixin, DeleteView):
    """
    Use a unique URL for Request object and change status to 'CANCEL'
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin
    """

    model = pts_models.Request
    success_url = reverse_lazy("pts:open")

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

        self.object.request_status = get_status("CANCEL")
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
