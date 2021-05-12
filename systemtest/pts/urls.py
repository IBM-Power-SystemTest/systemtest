"""
URLs for PTS app
    References:
        https://docs.djangoproject.com/en/3.1/topics/http/urls/
        https://docs.djangoproject.com/en/3.1/ref/urls/
"""

from django.urls import path
from django.views.generic.base import RedirectView

from systemtest.pts import views

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
        route="open/",
        view=views.OpenRequestView.as_view(),
        name="open"
    ),
    path(
        route="transit/",
        view=views.TransitRequestView.as_view(),
        name="transit"
    ),
    path(
        route="pending/",
        view=views.PendingPartListView.as_view(),
        name="pending"
    ),
    path(
        route="return/",
        view=views.ReturnPartListView.as_view(),
        name="return"
    ),
    path(
        route="close/",
        view=views.ClosePartListView.as_view(),
        name="close"
    ),
    path(
        route="history/",
        view=views.HistoryPartListView.as_view(),
        name="history"
    ),
    path(
        route="request/<pk>/",
        view=RedirectView.as_view(url="request/"),
        name="detail"
    ),
    path(
        route="request/<pk>/cancel/",
        view=views.RequestCancel.as_view(),
        name="cancel"
    ),
    path(
        route="request/<pk>/return/open/",
        view=views.ReturnToOpen.as_view(),
        name="return_to_open"
    ),
    path(
        route="request/<pk>/return/pending/",
        view=views.ReturnToPending.as_view(),
        name="return_to_pending"
    ),
]
