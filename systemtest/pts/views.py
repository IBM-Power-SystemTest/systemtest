# Python
from typing import Any, Dict, Tuple, Type, Union

# Django Forms
from django.forms.formsets import formset_factory
from django.forms.forms import BaseForm

# Django HTTP
from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy

# Django Views
from django.views.generic import ListView, FormView, DetailView, CreateView
from django.shortcuts import redirect, render

# Django db
from django.db.models.query import QuerySet

# APP PTS
from systemtest.pts import forms, models


class OpenPartListView(ListView):
    model = models.RequestTrack
    template_name = "pts/open.html"
    ordering = ("created",)

    def get_queryset(self) -> QuerySet:
        query = {"request_track_status__name": "OPEN"}
        queryset = self.model.objects.filter(**query)

        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["form_part_id"] = forms.RequestPartForm()
        context["form_comment"] = forms.RequestTrackCommentForm()

        return context


class TransitPartListView(ListView):
    template_name = "pts/transit.html"


class RecivePartListView(ListView):
    template_name = "pts/recive.html"


class ReturnPartListView(DetailView):
    template_name = "pts/return.html"


class ClosePartListView(ListView):
    template_name = "pts/close.html"


class RequestView(FormView):
    template_name = "pts/request/request.html"
    form_class = forms.RequestGroupForm

    def form_valid(self, form: BaseForm) -> HttpResponse:
        data = form.cleaned_data
        parts_qty = data.get("qty")
        are_more_fields_required = (
            parts_qty > 1 and
            data.get("is_serialized") and not
            data.get("is_vpd")
        )
        parts_qty = parts_qty if are_more_fields_required else 1
        kwargs = {
            "parts_qty": parts_qty,
        }
        return RequestDetailView.as_view()(self.request, **kwargs)


class RequestDetailView(FormView):
    template_name = "pts/request/request.html"
    success_url = reverse_lazy("pts:open")
    form_class = forms.RequestGroupForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["detailed_form"] = self.get_detailed_form()
        return context

    def get_detailed_form(self) -> Any:
        RequestPartFormset = formset_factory(
            forms.RequestPartForm,
            extra=self.kwargs.get("parts_qty"),
        )
        return RequestPartFormset

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = self.get_form()
        if form.is_valid() and request.POST.get("form-0-part_id"):
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form) -> HttpResponse:
        detailed_form = self.get_detailed_form()(form.data)
        print(form.cleaned_data)
        print(detailed_form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())
