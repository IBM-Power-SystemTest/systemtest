from django.urls import path
from systemtest.pts import views

app_name = "pts"
urlpatterns = [
    path(
        route="",
        view=views.RequestView.as_view(),
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
        route="recive/",
        view=views.RecivePartListView.as_view(),
        name="recive"
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
        route="request/<pk>/edit/",
        view=views.UpdateRequestView.as_view(),
        name="update"
    )
]
