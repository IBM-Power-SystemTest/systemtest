# Python
from typing import Any, Dict, Tuple, Type, Union

# Django Forms
from django.forms.formsets import formset_factory
from django.forms.forms import BaseForm
from django.forms.models import modelformset_factory

# Django HTTP
from django.http.request import HttpRequest, QueryDict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy

# Django Views
from django.views.generic import ListView, FormView, DetailView, CreateView
from django.shortcuts import redirect, render

# Django Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Django db
from django.db.models.query import QuerySet
from django.db.models import Q

# APP PTS
from systemtest.pts import forms, models

RequestFormset = modelformset_factory(
    models.Request,
    forms.RequestUpdateListForm,
    extra=0,
)

class OpenPartListView(FormView):
    template_name = "pts/views/open.html"
    success_url = reverse_lazy("pts:open")

    model = models.Request
    ordering = ("created",)
    query = (
        Q(request_status__name="OPEN") |
        Q(request_status__name="TRANSIT")
    )

    form_class = RequestFormset

    def get_queryset(self) -> QuerySet:
        queryset = self.model.objects.filter(self.query)
        return queryset.order_by(*self.ordering)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        queryset = self.get_queryset()
        self.form_class = RequestFormset(queryset=queryset)
        rows = zip(queryset, self.form_class)
        kwargs = {
            "object_list": queryset,
            "form": self.form_class,
            "rows": rows
        }
        print(queryset)
        return super().get_context_data(**kwargs)

    def form_valid(self, form: BaseForm) -> HttpResponse:
        print("VALID")
        return super().form_valid(form)


class TransitPartListView(ListView):
    template_name = "pts/transit.html"


class RecivePartListView(ListView):
    template_name = "pts/recive.html"


class ReturnPartListView(DetailView):
    template_name = "pts/return.html"


class ClosePartListView(ListView):
    template_name = "pts/close.html"


class RequestView(LoginRequiredMixin, FormView):
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


class RequestDetailView(LoginRequiredMixin, FormView):
    template_name = "pts/request/request.html"
    success_url = reverse_lazy("pts:open")
    form_class = forms.RequestGroupForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        if "detailed_form" not in kwargs:
            kwargs["detailed_form"] = self.get_detailed_form()
        return super().get_context_data(**kwargs)

    def get_detailed_form(self) -> Any:
        RequestPartFormset = formset_factory(
            forms.RequestPartForm,
            extra=self.kwargs.get("parts_qty"),
        )
        return RequestPartFormset

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = self.get_form()
        if form.is_valid() and request.POST.get("form-0-part_id"):
            detailed_form = self.get_detailed_form()(form.data)
            if detailed_form.is_valid():
                return self.form_valid(form, detailed_form)
            else:
                return self.form_invalid(detailed_form=detailed_form)
        else:
            return self.form_invalid(form=form)

    def form_valid(self, form, *args) -> HttpResponse:
        detailed_form = args[0]

        request_group = form.save(commit=False)
        user = self.request.user

        part_id_set = detailed_form.cleaned_data
        part_number_set = {part_id.get("pn") for part_id in part_id_set}
        serial_number_set = {part_id.get("sn") for part_id in part_id_set}

        if len(part_number_set) > 1:
            error_message = "Se estan requiriendo distintos numeros de parte"
            form.add_error(None, error_message)
            self.form_invalid(form=form)

        part_number = part_number_set.pop()
        request_group.part_number = part_number
        request_group.save()

        for serial_number in serial_number_set:
            request = models.Request(
                request_group=request_group,
                part_number=part_number,
                serial_number=serial_number,
                user=user
            )

            request.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, **kwargs) -> HttpResponse:
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(**kwargs))
