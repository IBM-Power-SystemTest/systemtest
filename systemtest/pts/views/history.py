# Django Views
from django.db.models.query_utils import Q
from django.views.generic.list import ListView

# APPs
from systemtest.pts import models as pts_models


class HistoryPartListView(ListView):
    template_name = "pts/history.html"
    model = pts_models.RequestHistory
    paginate_by = 100
