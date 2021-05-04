# Python
from typing import Any

# Django Forms
from django.forms.models import BaseModelForm

# Django HTTP
from django.urls.base import reverse_lazy
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

# Django Views
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

# Django db
from django.db.models.query import QuerySet
from django.db.models import Q

# APPs
from systemtest.quality import forms as quality_forms, models as quality_models


class QualitySystems(LoginRequiredMixin, FormView):
    model = quality_models.QualitySystem
    form_class = quality_forms.QualitySystemFormset
    template_name = "quality/systems.html"
    success_url = reverse_lazy("quality:index")
    query = (
        ~Q(quality_status__name="APROVED") &
        ~Q(quality_status__name="PASSED")
    )

    def get_queryset(self) -> QuerySet:
        return self.model.objects.filter(self.query)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        self.queryset = self.get_queryset()
        self.form_class = self.form_class(queryset=self.queryset)

        kwargs["form"] = self.form_class
        kwargs["rows"] = zip(self.form_class.get_queryset(), self.form_class)

        return super().get_context_data(**kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        formset = self.get_form()
        valid_forms = []
        for form in formset:
            if form.has_changed() and form.is_valid():
                queryset = self.get_queryset()
                initial_status = form.initial.get("quality_status")
                if queryset.filter(quality_status__pk=initial_status):
                    valid_forms.append(form)

        if valid_forms:
            return self.form_valid(valid_forms)
        else:
            return self.form_invalid(formset)

    def form_valid(self, forms: list[BaseModelForm]) -> HttpResponse:
        for form in forms:
            system = form.save(commit=False)

            system.user = self.request.user
            system.save()

        return HttpResponseRedirect(self.get_success_url())
