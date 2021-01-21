# Python
from typing import Any, Dict, Type, Union

# Django Forms
from django import forms
from django.forms.models import BaseModelForm, BaseModelFormSet

# Django HTTP
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

# Django Views
from django.views.generic import FormView

# Django db
from django.db.models.query import QuerySet

# APP PTS
from systemtest.pts import forms as pts_forms, models as pts_models


class ReturnPartListView(FormView):
    pass


class ClosePartListView(FormView):
    pass


class BaseRequestListView(FormView):
    model = pts_models.Request
    status_model = pts_models.RequestStatus

    query = None
    ordering = ("created",)

    choice_field = "request_status"
    choice_model = status_model
    choice_query = None

    next_status_query = None

    form_class = pts_forms.RequestFormset

    def get_queryset(self) -> QuerySet:
        queryset = self.model.objects.filter(self.query)
        return queryset.order_by(*self.ordering)

    def get_custom_choices(self) -> Union[QuerySet, None]:
        if not self.choice_query or not self.choice_model:
            return None

        choices = self.choice_model.objects.filter(self.choice_query)
        return choices

    def set_custom_choices(self, formset: BaseModelFormSet):
        if choices := self.get_custom_choices():
            for form in formset:
                form.fields[self.choice_field] = forms.ModelChoiceField(choices)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        queryset = self.get_queryset()
        self.form_class = self.form_class(queryset=queryset)
        self.set_custom_choices(self.form_class)

        kwargs["form"] = self.form_class
        kwargs["rows"] = zip(queryset, self.form_class)

        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        formset = self.get_form()
        valid_forms = []
        for form in formset:
            if form.is_valid() and form.has_changed():
                valid_forms.append(form)

            print(form.errors)
        if valid_forms:
            return self.form_valid(valid_forms)
        else:
            return self.form_invalid(formset)

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        if serial == request.serial_number:
            return True
        return False

    def get_new_status(self, request: type[pts_models.Request]) -> Any:
        return self.status_model.objects.get(self.next_status_query)

    def form_valid(self, forms: list[BaseModelForm]) -> HttpResponse:
        for form in forms:
            data = form.cleaned_data
            if not data.get("part_id"):
                form.save()
                continue

            request = form.save(commit=False)
            sn = data.get("sn")
            if sn:
                if not self.is_valid_serial(request, sn):
                    return self.form_invalid(form)
                    form.add_error("part_id", "SN no es el mismo que el anterior")

                request.serial_number = sn

            request.part_number = data.get("pn")
            request.comment = None

            request.request_status = self.get_new_status(request)
            request.save()

        return HttpResponseRedirect(self.get_success_url())
