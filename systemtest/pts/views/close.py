# Django db
from django.db.models import Q

# APPs
from systemtest.pts import models as pts_models, forms as pts_forms
from systemtest.utils.views import AbstractFilteView


class ClosePartListView(AbstractFilteView):
    """
    Django ListView for close parts (CLOSE GOOD, CLOSE BAD, CANCEL)
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin
    """

    filterset_class = pts_forms.RequestFilterSet
    template_name = "pts/close.html"

    query = (
        Q(request_status__name="CLOSE GOOD") |
        Q(request_status__name="CLOSE BAD") |
        Q(request_status__name="CANCEL")
    )
    queryset = pts_models.Request.objects.filter(query)
    ordering = ["-modified"]
