# Python
from typing import Any

# Django Forms
from django.forms.forms import BaseForm
from django.forms.formsets import formset_factory

# Django HTTP
from django.urls.base import reverse_lazy
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

# Django Views
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView

# Django Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# APP PTS
from systemtest.pts import forms as pts_forms, models as pts_models


class RequestDelete(DeleteView):
    model = pts_models.Request
    success_url = reverse_lazy("pts:open")
    template_name = "pts/request_delete.html"
    change_status = pts_models.RequestStatus.objects.get(name="CANCEL")

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
        self.object.request_status = self.change_status
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class RequestGroupDetail(DetailView):
    model = pts_models.RequestGroup

class RequestUpdate(UpdateView):
    pass
