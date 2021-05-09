# Python
from datetime import date

# Django Contrib
from django.contrib import messages
from django.contrib.auth import login as auth_login, views as auth_views

# Django
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.conf import settings


class LoginView(auth_views.LoginView):
    def form_valid(self, form):
        """ Security check complete. Log the user in.
            Also check the days left to change password, get last_login time
            and print send some status messages
        """

        user = form.get_user()
        last_login = user.last_login if user.last_login else date.today()

        auth_login(self.request, user)

        last_password_date = user.last_password_modified
        password_days_delta = (date.today() - last_password_date).days

        if password_days_delta >= settings.PASSWORD_EXPIRE_DAYS:
            user.is_active = False
            user.save()

            messages.error(self.request, f"Your user has been deactivated")
            return HttpResponseRedirect(reverse_lazy("users:login"))

        elif password_days_delta >= settings.CHANGE_PASSWORD_MESSAGE_DAYS:
            remain_days = settings.PASSWORD_EXPIRE_DAYS - password_days_delta
            messages.warning(
                self.request,
                f"Your password will expire in {remain_days} days"
            )

        messages.info(
            self.request,
            "Welcome back ( Last login: {:%B %d, %H:%M} )".format(last_login)
        )
        return HttpResponseRedirect(self.get_success_url())
