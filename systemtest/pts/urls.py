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
        route="history/",
        view=views.ClosePartListView.as_view(),
        name="history"
    ),
    path(
        route="request/<pk>/",
        view=views.DetailRequestView.as_view(),
        name="detail"
    ),
    path(
        route="request/<pk>/cancel/",
        view=views.RequestCancel.as_view(),
        name="cancel"
    ),
    path(
        route="request/<pk>/reopen/",
        view=views.RequestReopen.as_view(),
        name="reopen"
    ),
    path(
        route="request_group/<pk>",
        view=views.RequestGroupDetail.as_view(),
        name="detail_group"
    ),
    path(
        route="request_group/<pk>/update",
        view=views.DetailRequestView.as_view(),
        name="update"
    ),
]
