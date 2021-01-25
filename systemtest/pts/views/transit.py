# Django HTTP
from django.urls.base import reverse_lazy

# Django db
from django.db.models import Q

# APP PTS
from .views import BaseRequestListView

class TransitRequestView(BaseRequestListView):
    template_name = "pts/transit.html"
    success_url = reverse_lazy("pts:transit")

    query = Q(request_status__name="TRANSIT")
    next_status_query = Q(name="RECIVE")

    def get_template_names(self) -> list[str]:
        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="TA"):
            self.template_name = "pts/transit_ta.html"

        return super().get_template_names()
