from django.urls import path
from systemtest.quality import views

app_name = "pts"
urlpatterns = [
    path(
        route="",
        view=views.QualitySystems.as_view(),
        name="index"
    ),
    path(
        route="history/",
        view=views.QualityHistory.as_view(),
        name="history"
    )
]
