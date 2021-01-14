from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib.auth import views as auth_view
from django.urls.base import reverse_lazy

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class LoginView(auth_view.LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('pts:request_group')


class PasswordChangeView(auth_view.PasswordChangeView):
    template_name = 'users/password/change.html'
    success_url = reverse_lazy('users:login')


class PasswordResetView(auth_view.PasswordResetView):
    template_name = 'users/password/reset.html'
    success_url = reverse_lazy('users:login')


class PasswordResetDoneView(auth_view.PasswordResetConfirmView):
    pass
