from django.urls import path
from systemtest.pts import views

app_name = "pts"
urlpatterns = [
    path(
        route="",
        view=views.RequestView.as_view(),
        name="index"
    ),
]
