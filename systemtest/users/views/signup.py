# Python
from typing import Any, Dict, Tuple, Union

# Django
from django import forms, http
from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect

from django.forms.models import BaseModelForm

from django.urls.base import reverse_lazy

from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Apps
from systemtest.users.forms import SignUpForm


class SignUpView(LoginRequiredMixin, CreateView):
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")
    form_class = SignUpForm

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        if not self.request.user.is_staff:
            return HttpResponseNotAllowed(["GET", "POST"])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        new_user = form.save()

        new_user.department = self.request.user.department
        new_user.shift = self.request.user.shift
        new_user.groups.add(form.cleaned_data["groups"])

        new_user.save()

        return HttpResponseRedirect(str(self.success_url))
