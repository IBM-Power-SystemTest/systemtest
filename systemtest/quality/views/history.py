# Django
from django.db.models.query_utils import Q
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# APPs
from systemtest.quality import models as quality_models


class QualityHistory(LoginRequiredMixin, ListView):
    """
    Django ListView for close parts (CLOSE GOOD, CLOSE BAD, CANCEL)
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin
    """

    template_name = "quality/history.html"
    model = quality_models.QualityHistory
    paginate_by = 100
    ordering = ["-created"]
