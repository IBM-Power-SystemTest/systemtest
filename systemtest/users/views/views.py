# Python
from datetime import date

# Django Contrib
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    get_user_model,
    forms as auth_forms,
    views as auth_views,
    login as auth_login
)
from django.conf import settings

# Django
from django.views.generic import UpdateView
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ("first_name", "last_name")
    template_name = "users/update.html"

    def get_object(self):
        return self.request.user


class LoginView(auth_views.LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        user = self.request.user
        last_password_date = user.last_password_modified

        password_days_delta = (date.today() - last_password_date).days
        print(password_days_delta)
        print(settings.PASSWORD_EXPIRE_DAYS)
        print(settings.CHANGE_PASSWORD_MESSAGE_DAYS)
        if password_days_delta >= settings.PASSWORD_EXPIRE_DAYS:
            user.is_active = False
            user.save()
            messages.info(self.request, f"Su usuario ha sido desactvado")
            return HttpResponseRedirect(reverse_lazy("users:login"))

        elif password_days_delta >= settings.CHANGE_PASSWORD_MESSAGE_DAYS:
            remain_days = settings.PASSWORD_EXPIRE_DAYS - password_days_delta
            messages.info(self.request, f"La contrasena va ha expirar en {remain_days} dias")

        return HttpResponseRedirect(self.get_success_url())
