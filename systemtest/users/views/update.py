
from django.urls.base import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Django UpdateView for user data
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView
    """
    model = get_user_model()
    fields = (
        "first_name",
        "last_name",
        "shift",
        "mfs",
        "email",
    )

    success_url = reverse_lazy("users:update")
    template_name = "users/update.html"


    def get_object(self):
        return self.request.user
