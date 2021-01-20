from django.urls import path
from systemtest.users import views
from django.contrib.auth import views as auth_view
from django.urls import path

from systemtest.users import views

app_name = "users"

urlpatterns = [
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='password/change/',
        view=views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        route='password/reset/',
        view=views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        route="~redirect/",
        view=views.UserRedirectView.as_view(),
        name="redirect"
    ),
    path(
        route="~update/",
        view=views.UserUpdateView.as_view(),
        name="update"
    ),
    path(
        route="<str:username>/",
        view=views.user_detail_view,
        name="detail"
    ),

]
