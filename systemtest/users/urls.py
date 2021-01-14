from django.urls import path

from systemtest.users import views

app_name = "users"
urlpatterns = [
    path(
        route="~redirect/",
        view=views.user_redirect_view,
        name="redirect"
    ),
    path(
        route="~update/",
        view=views.user_update_view,
        name="update"
    ),
    path(
        route="<str:username>/",
        view=views.user_detail_view,
        name="detail"
    ),
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),
    path(
        route='password/change/',
        view=views.PasswordChangeView.as_view(),
        name='password/change'
    ),
    path(
        route='password/reset/',
        view=views.PasswordResetView.as_view(),
        name='password/reset'
    ),
]
