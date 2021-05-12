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
    """
    Django FormView abstract to set a FormSet or ModelFormSet with a
    QuerySet to eval multiple forms each form coresponding to one row/object
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin

    Attributes:
        model:
            Model to filter and gets QuerySet
        query:
            Query to gets QuerySet from model, usually perform queries status
    """

    form_class = quality_forms.QualitySystemFormset
    template_name = "quality/systems.html"
    success_url = reverse_lazy("quality:index")

    model = quality_models.QualitySystem
    query = (
        ~Q(quality_status__name="APROVED") &
        ~Q(quality_status__name="PASSED")
    )

    def get_queryset(self) -> QuerySet:
        """
        Gets QuerySet with query and model

        Args:
            self:
                instance

        Returns:
            QuerySet filtering Model with query
        """

        return self.model.objects.filter(self.query)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Passes the keyword arguments received as the template context.
        Gets queryset and custom the formset to pass a formset and rows,
        than are zipped object of queryset and formset

        Args:
            self:
                Instance
            kwargs:
                kwargs to passes into context template

        Returns:
            Original get_context_data passing original kwargs after adds
            custom kwargs to its, and original function passes to context
        """

        self.form_class = self.form_class(queryset=self.get_queryset())

        kwargs["form"] = self.form_class
        kwargs["rows"] = zip(self.form_class.get_queryset(), self.form_class)

        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid and has changes.

        Args:
            self:
                Instance
            request:
                HttpRequest, includes all request data
            args:
                Positional arguments
            kwargs:
                Keyword arguments
        """

        # Get ModelFormSet (form_class)
        formset = self.get_form()
        valid_forms = []
        for form in formset:

            # Only count forms with changes and also are valid
            if form.has_changed() and form.is_valid():

                # Checking if form data still have the same
                # status in the database to prevent an object
                # that is already in another state from being changed
                queryset = self.get_queryset()
                initial_status = form.initial.get("quality_status")
                if queryset.filter(quality_status__pk=initial_status):
                    valid_forms.append(form)

        if valid_forms:
            return self.form_valid(valid_forms)
        else:
            return self.form_invalid(formset)

    def form_valid(self, forms: list[BaseModelForm]) -> HttpResponse:
        """
        Process list of forms passed in self.post (forms changed and valid)

        Args:
            forms:
                List of forms changed and valid passed by the post method

        Returns:
            After add extra data to each form return HttpResponse to sucess_url
        """

        for form in forms:
            system = form.save(commit=False)

            system.user = self.request.user
            system.save()

        return HttpResponseRedirect(self.get_success_url())
