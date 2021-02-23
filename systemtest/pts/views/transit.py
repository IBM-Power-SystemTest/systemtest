# Python
from typing import Type

# Django HTTP
from django.urls.base import reverse_lazy

# Django db
from django.db.models import Q

# APP PTS
from .views import BaseRequestListView
from systemtest.pts import models as pts_models

class TransitRequestView(BaseRequestListView):
    template_name = "pts/transit.html"
    success_url = reverse_lazy("pts:transit")

    query = Q(request_status__name="TRANSIT")
    next_status_query = Q(name="PENDING")

    def get_template_names(self) -> list[str]:
        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="TA"):
            self.template_name = "pts/transit_ta.html"

        return super().get_template_names()

    def get_new_status(self, request: Type[pts_models.Request]):
        if request.request_group.is_vpd:
            return self.status_model.objects.get(name="CLOSE GOOD")
        return super().get_new_status(request)
