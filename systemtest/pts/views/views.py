# Python
from typing import Any, Dict, Tuple, Type, Union

# Django Forms
from django import forms
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm, modelformset_factory
from django.forms.formsets import formset_factory

# Django HTTP
from django.urls.base import reverse_lazy
from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponse, HttpResponseRedirect

# Django Views
from django.shortcuts import redirect, render
from django.views.generic import ListView, FormView, DetailView, CreateView

# Django Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Django db
from django.db.models import Q
from django.db.models.query import QuerySet

# APP PTS
from systemtest.pts import forms as pts_forms, models as pts_models

class RecivePartListView(ListView):
    template_name = "pts/recive.html"


class ReturnPartListView(DetailView):
    template_name = "pts/return.html"


class ClosePartListView(ListView):
    template_name = "pts/close.html"

