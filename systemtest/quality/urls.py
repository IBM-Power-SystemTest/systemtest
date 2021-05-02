from systemtest.quality.views.passed import QualityReturn
from django.urls import path
from django.views.generic.base import RedirectView
from systemtest.quality import views

app_name = "quality"
urlpatterns = [
    path(
        route="",
        view=views.QualitySystems.as_view(),
        name="index"
    ),
    path(
        route="passed",
        view=views.QualityPassed.as_view(),
        name="passed"
    ),
    path(
        route="history/",
        view=views.QualityHistory.as_view(),
        name="history"
    ),
    path(
        route="<pk>/",
        view=RedirectView.as_view(url=""),
        name="system_detail"
    ),
    path(
        route="<pk>/return/",
        view=views.QualityReturn.as_view(),
        name="system_return"
    ),
]
