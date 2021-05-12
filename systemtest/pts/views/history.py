# Django Views
from django.views.generic.list import ListView

# Django Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Django db
from django.db.models import Q

# APPs
from systemtest.pts import models as pts_models


class HistoryPartListView(LoginRequiredMixin, ListView):
    """
    Django ListView for history of parts
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin
    """

    template_name = "pts/history.html"
    model = pts_models.RequestHistory
    paginate_by = 100
    ordering = ["-created"]
