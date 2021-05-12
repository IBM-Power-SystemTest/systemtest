# Django Views
from django.views.generic.list import ListView

# Django Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Django db
from django.db.models import Q

# APPs
from systemtest.pts import models as pts_models


class ClosePartListView(LoginRequiredMixin, ListView):
    """
    Django ListView for close parts (CLOSE GOOD, CLOSE BAD, CANCEL)
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin
    """

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
