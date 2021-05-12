# Python
from typing import Any, Type, Union

# Django Forms
from django import forms
from django.forms.models import BaseModelForm, BaseModelFormSet

# Django HTTP
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

# Django Views
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

# Django db
from django.db.models import Model, Q
from django.db.models.query import QuerySet

# APP PTS
from systemtest.pts import forms as pts_forms, models as pts_models


class BaseRequestListView(LoginRequiredMixin, FormView):
    """
    Django FormView abstract to set a FormSet or ModelFormSet with a
    QuerySet to eval multiple forms each form coresponding to one row/object
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin

    Attributes:
        model:
            Model to filter and gets QuerySet
        status_model:
            Model that contains the status to divide the model objects
        query:
            Query to gets QuerySet from model, usually perform queries status
        choice_field:
            Name in the Model for status/choices
        choice_model:
            Choices for Formset and change of status a Model
        choice_query:
            How to gets the choices to changes the status
        next_status_query:
            How to gets the next_status
        next_status:
            Optional; A status Object for example RequestStatus Model
            overrides the next_status_query
        validate_serial:
            If is necesary perform a serial validation between current
            and input serial
        form_class:
            FormSet to zip with QuerySet to get data and its form in one line
    """

    model = pts_models.Request
    status_model = pts_models.RequestStatus

    query = None

    choice_field = "request_status"
    choice_model = status_model
    choice_query = None

    next_status_query = None
    next_status = None

    form_class = pts_forms.RequestFormset

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

    def get_custom_choices(self) -> QuerySet:
        """
        Gets a QuerySet using a choice_model and choice_query

        Args:
            self:
                instance

        Returns:
            QuerySet filtering Model with query
        """

        if not self.choice_query or not self.choice_model:
            return self.status_model.objects.none()

        choices = self.choice_model.objects.filter(self.choice_query)
        return choices

    def set_custom_choices(self, formset: BaseModelFormSet) -> None:
        """
        Changes/adds the choices/option in choice field from formset

        Args:
            formset:
                Formset add ModelChoicefield

        Returns:
            None; Chage form fields inline
        """

        if choices := self.get_custom_choices():
            for form in formset:
                form.fields[self.choice_field] = forms.ModelChoiceField(
                    choices)

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

        self.queryset = self.get_queryset()

        # Instantiate a ModelFormSet with query set to create a form
        # for each Request object
        self.form_class = self.form_class(queryset=self.queryset)
        self.set_custom_choices(self.form_class)

        kwargs["form"] = self.form_class
        kwargs["rows"] = zip(self.form_class.get_queryset(), self.form_class)

        return super().get_context_data(**kwargs)

    def dispatch(self, *args, **kwargs):
        """
        Create an attribute with all groups of the user who made the http request

        Args:
            self:
                Instance
            args:
                Positional arguments
            kwargs:
                Keyword arguments

        Returns:
            Original function dispatch after sets user_groups attribute
        """

        self.user_groups = self.request.user.groups.all()
        return super().dispatch(*args, **kwargs)

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
                initial_status = form.initial.get("request_status")
                if queryset.filter(request_status__pk=initial_status):
                    valid_forms.append(form)

        if valid_forms:
            return self.form_valid(valid_forms)
        else:
            return self.form_invalid(formset)

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        """
        Rules to verify serial number, sometimes both serial have to be the same
        in other cases serials must be different or it may not matter

        Args:
            request:
                Request object to get the original serial number
            serial:
                New serial number to compare with request serial number

        Returns:
            Boolean depends of the validation case by default they have be equals
        """

        if serial == request.serial_number:
            return True
        return False

    def get_new_status(self, request: Type[pts_models.Request]) -> Any:
        """
        Executes a query to get status to move the Model in case
        everything has gone well

        Args:
            self:
                Instance

        Returns:
            Next status to move the Model
        """

        if not self.next_status:
            self.next_status = self.status_model.objects.get(
                self.next_status_query)
        return self.next_status

    def form_valid(self, forms: list[BaseModelForm]) -> HttpResponse:
        """
        Process list of forms passed in self.post (forms changed and valid)
        make extra validations like serial number validation, users,
        status and others validation than depends on original Model and
        data inserted into its form

        Args:
            forms:
                List of forms changed and valid passed by the post method

        Returns:
            After validates each form return HttpResponse to sucess_url
            Maybe if a validation is wrong it can send the form_invalid method
        """

        for form in forms:

            # Getting data processed by the form
            data = form.cleaned_data
            if not data.get("part_id"):
                form.save()
                continue

            # Save object but not commit to database yet
            request = form.save(commit=False)

            if sn := data.get("sn"):

                # If serial validation fails send to form_invalid to handle
                if not self.is_valid_serial(request, sn):
                    return self.form_invalid(form)
                request.serial_number = sn

            # Setting extra values from the form and http request info
            request.part_number = data.get("pn")
            request.comment = None

            request.user = self.request.user

            # Setting the next status of Model
            request.request_status = self.get_new_status(request)
            request.save()

        return HttpResponseRedirect(self.get_success_url())
