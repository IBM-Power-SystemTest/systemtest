# Django Views
from django.db.models.query_utils import Q
from django.views.generic.list import ListView

# APPs
from systemtest.pts import models as pts_models


class ClosePartListView(ListView):
    template_name = "pts/close.html"
    model = pts_models.Request
    paginate_by = 30
    query = (
        Q(request_status__name="CLOSE GOOD") |
        Q(request_status__name="CLOSE BAD") |
        Q(request_status__name="CANCEL")
    )
    queryset = pts_models.Request.objects.filter(query)
    ordering = ["-modified"]
