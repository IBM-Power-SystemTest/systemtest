# Django HTTP
from django.urls.base import reverse_lazy

# Django db
from django.db.models import Q

# APP PTS
from .views import BaseRequestListView

class TransitRequestView(BaseRequestListView):
    template_name = "pts/transit.html"
    success_url = reverse_lazy("pts:transit")

    query = Q(request_status__pk=2)
    next_status_query = Q(pk=3)
