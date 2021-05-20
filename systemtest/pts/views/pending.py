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
    """
    RequestListView for Request pending to give disposition
    """

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
            self.template_name = "pts/pending_ta.html"

        return super().get_template_names()

    def form_valid(self, forms: list[BaseModelForm]) -> HttpResponse:
        """
        Process list of forms passed in self.post (forms changed and valid)
        make extra validations like serial number validation, users,
        status and others validation than depends on original Model and
        data inserted into its form

        Args:
            forms:
                List of forms changed and valid passed by the post method

        Returns:
            After validates each form return HttpResponse to sucess_url
            Maybe if a validation is wrong it can send the form_invalid method
        """

        for form in forms:

            # Getting data processed by the form
            data = form.cleaned_data
            if not data.get("part_id"):
                continue

            # Save object but not commit to database yet
            request = form.save(commit=False)

            request.part_number = data.get("pn")
            if sn := data.get("sn"):
                request.serial_number = sn

            # If form has a request status save as next status
            # If no have request status continue with next status by default
            if new_status := data.get("request_status"):
                self.next_status = new_status

            # If form has ncm_tag move as BAD status
            if ncm_tag := data.get("ncm_tag"):
                request.ncm_tag = ncm_tag
                self.next_status = None
                self.next_status_query = Q(name="BAD")

            request.request_status = self.get_new_status(request)
            request.save()

            self.next_status_query = None
        return HttpResponseRedirect(self.get_success_url())
