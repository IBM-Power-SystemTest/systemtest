"""
URLs for Quality app
    References:
        https://docs.djangoproject.com/en/3.1/topics/http/urls/
        https://docs.djangoproject.com/en/3.1/ref/urls/
"""

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
