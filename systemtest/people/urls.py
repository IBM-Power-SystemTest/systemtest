"""
URLs for PTS app
    References:
        https://docs.djangoproject.com/en/3.1/topics/http/urls/
        https://docs.djangoproject.com/en/3.1/ref/urls/
"""

from django.urls import path
from django.views.generic.base import RedirectView, TemplateView
from django.conf import settings

from systemtest.people import views

app_name = "pts"
urlpatterns = [
    path(
        route="",
        view=RedirectView.as_view(url="request/"),
        name="index"
    ),
    path(
        route="request/",
        view=views.RequestView.as_view(),
        name="request"
    ),
    path(
        route="requirements/",
        view=views.RequirementsView.as_view(),
        name="requirements"
    ),
    path(
        route="<pk>/cancel/",
        view=views.PeopleRequirementCancel.as_view(),
        name="cancel"
    ),
    path(
        route="history/",
        view=views.PeopleHistoryView.as_view(),
        name="history"
    ),
    path(
        route="summary/",
        view=views.PeopleSummary.as_view(),
        name="summary"
    ),
]
