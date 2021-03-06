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


class RequestGroupDetail(DetailView):
    model = pts_models.RequestGroup


class RequestUpdate(UpdateView):
    pass
