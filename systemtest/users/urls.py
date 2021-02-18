from django.urls import path
from django.contrib.auth import views as auth_views

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
            template_name="users/password_change.html"
        ),
        name='password_change'
    ),
]
