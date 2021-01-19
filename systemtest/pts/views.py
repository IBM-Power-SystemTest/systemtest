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


class OpenPartListView(FormView):
    template_name = "pts/views/open.html"
    success_url = reverse_lazy("pts:request")

    model = pts_models.Request
    ordering = ("created",)
    query = (
        Q(request_status__pk=1) |
        Q(request_status__pk__gte=10)
    )
    choice_field = "request_status"
    choice_model = pts_models.RequestStatus
    choice_query = Q(pk__gte=10) | Q(pk=1)

    form_class = pts_forms.RequestFormset

    def get_queryset(self) -> QuerySet:
        queryset = self.model.objects.filter(self.query)
        return queryset.order_by(*self.ordering)

    def get_custom_choices(self):
        if not self.choice_model:
            return None

        choices = self.choice_model.objects.filter(self.choice_query)
        return choices

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        queryset = self.get_queryset()
        formset = pts_forms.RequestFormset(queryset=queryset)

        if choices := self.get_custom_choices():
            for form in formset:
                form.fields[self.choice_field] = forms.ModelChoiceField(choices)

        self.form_class = formset
        kwargs["form"] = self.form_class
        kwargs["rows"] = zip(queryset, self.form_class)

        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        valid_forms = []
        for f in form:
            if f.is_valid() and f.has_changed():
                valid_forms.append(f)

        if valid_forms:
            return self.form_valid(valid_forms)
        else:
            return self.form_invalid(form)

    def form_valid(self, forms: list[BaseModelForm]) -> HttpResponse:
        for form in forms:
            data = form.cleaned_data
            if not data.get("part_id"):
                form.save()
                continue

            request = form.save(commit=False)
            sn = data.get("sn")

            if sn and sn == request.serial_number:
                form.add_error("part_id", "SN es el mismo al solicitado")
                print(form.errors)
                return self.form_invalid(form=form)

            request.serial_number = data.get("pn")
            request.serial_number = sn
            request.comment = None

            if request.request_group.is_vpd:
                status = pts_models.RequestStatus.objects.get(name="GOOD")
            else:
                status = pts_models.RequestStatus.objects.get(name="TRANSIT")

            request.request_status = status
            request.save()

        return HttpResponseRedirect(self.get_success_url())


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
    form_class = pts_forms.RequestGroupForm

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
    form_class = pts_forms.RequestGroupForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        if "detailed_form" not in kwargs:
            kwargs["detailed_form"] = self.get_detailed_form()
        return super().get_context_data(**kwargs)

    def get_detailed_form(self) -> Any:
        RequestPartFormset = formset_factory(
            pts_forms.RequestPartForm,
            extra=self.kwargs.get("parts_qty"),
        )
        return RequestPartFormset

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = self.get_form()
        if form.is_valid() and request.POST.get("form-0-part_id"):
            detailed_form = self.get_detailed_form()(form.data)
            if detailed_form.is_valid():
                return self.form_valid(form, detailed_form)

            return self.form_invalid(detailed_form=detailed_form)

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
            form.add_error("part_id", error_message)
            self.form_invalid(form=form)

        part_number = part_number_set.pop()
        request_group.part_number = part_number
        request_group.save()

        for serial_number in serial_number_set:
            request = pts_models.Request(
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
