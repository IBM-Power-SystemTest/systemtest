from typing import Any, Dict

from django.contrib.auth import get_user_model, forms as auth_forms
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import UpdateView

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    fields = ("first_name", "last_name")
    template_name = "users/update.html"

    def get_object(self):
        return self.request.user
