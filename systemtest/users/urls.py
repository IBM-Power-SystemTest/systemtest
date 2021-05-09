from django.contrib.messages.api import success
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls.base import reverse_lazy

from systemtest.users import views as users_views

app_name = "users"

urlpatterns = [
    path(
        route='login/',
        view=users_views.LoginView.as_view(
            template_name="users/login.html"
        ),
        name='login'
    ),
    path(
        route='signup/',
        view=users_views.SignUpView.as_view(),
        name='signup'
    ),
    path(
        route='logout/',
        view=auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        route="update/",
        view=users_views.UserUpdateView.as_view(),
        name="update"
    ),
    path(
        route='password/change/',
        view=auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=reverse_lazy("users:update")
        ),
        name='password_change'
    ),
]
