from django.db.models.query_utils import Q
from django.views.generic.list import ListView

from systemtest.quality import models

class QualityHistory(ListView):
    template_name = "quality/history.html"
    model = models.QualitySystem
    paginate_by = 30
    query = (
        Q(quality_status__name="CLOSE GOOD") |
        Q(quality_status__name="CLOSE BAD")
    )
    queryset = models.QualitySystem.objects.filter(query)
