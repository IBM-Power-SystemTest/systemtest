# Python
from typing import Any

# Django Forms
from django.forms.models import BaseModelForm

# Django HTTP
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

# Django Views
from django.views.generic import FormView

# Django db
from django.db.models.query import QuerySet
from django.db.models import Q

# APPs
from systemtest.quality import forms as quality_forms, models as quality_models


class QualitySystems(FormView):
    model = quality_models.QualitySystem
    form_class = quality_forms.QualitySystemFormset

    def get_queryset(self) -> QuerySet:
        return self.model.objects.exclude(operation_status="W")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        self.form_class = self.form_class(self.get_queryset())

        kwargs["form"] = self.form_class
        kwargs["rows"] = zip(queryset, self.form_class)

        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        formset = self.get_form()
        for form in formset:
            if form.has_changed() and form.is_valid():
                self.form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form: BaseModelForm) -> None:
        system = form.save(commit=False)

        system.user = self.request.user
        system.save()
