# Django
from django.db.models.query_utils import Q
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# APPs
from systemtest.pts import models as pts_models


class HistoryPartListView(LoginRequiredMixin, ListView):
    template_name = "pts/history.html"
    model = pts_models.RequestHistory
    paginate_by = 100
    ordering = ["-created"]
