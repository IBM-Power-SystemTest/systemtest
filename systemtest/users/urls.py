"""
URLs for Users app
    References:
        https://docs.djangoproject.com/en/3.1/topics/http/urls/
        https://docs.djangoproject.com/en/3.1/ref/urls/
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls.base import reverse_lazy

from systemtest.users import views

app_name = "users"

urlpatterns = [
    path(
        route='login/',
        view=views.LoginView.as_view(
            template_name="users/login.html"
        ),
        name='login'
    ),
    path(
        route='signup/',
        view=views.SignUpView.as_view(),
        name='signup'
    ),
    path(
        route='logout/',
        view=auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        route="update/",
        view=views.UserUpdateView.as_view(),
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
