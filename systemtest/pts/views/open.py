# Python
from typing import Any, Dict

# Django Forms
from django import forms
from django.forms.models import BaseModelForm

# Django HTTP
from django.urls.base import reverse_lazy
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

# Django Views
from django.views.generic import FormView

# Django db
from django.db.models import Q
from django.db.models.query import QuerySet

# APP PTS
from systemtest.pts import forms as pts_forms, models as pts_models


class OpenPartListView(FormView):
    template_name = "pts/open.html"
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
