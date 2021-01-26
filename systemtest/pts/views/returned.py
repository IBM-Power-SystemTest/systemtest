# Django HTTP
from typing import Any
from django.urls.base import reverse_lazy

# Django db
from django.db.models import Q

# APP PTS
from systemtest.pts import models as pts_models
from .views import BaseRequestListView
from .pending import PendingPartListView


class ReturnPartListView(BaseRequestListView):
    template_name = "pts/return.html"
    success_url = reverse_lazy("pts:return")

    query = (
        Q(request_status__pk__gte=6) &
        Q(request_status__lte=9)
    )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user_groups = self.request.user.groups.all()

        if user_groups.filter(name="IPIC"):
            self.query = Q(request_status__name="GOOD")
            self.template_name = "pts/return_ipic.html"

        elif user_groups.filter(name="IPIC NCM"):
            self.query = Q(request_status__name="BAD")
            self.template_name = "pts/return_ipic_ncm.html"

        return super().get_context_data(**kwargs)

    def get_new_status(self, request: type[pts_models.Request]) -> Any:
        status = str(request.request_status)
        if status == "BAD":
            self.next_status_query = Q(name="CLOSE BAD")
        elif status == "GOOD":
            self.next_status_query = Q(name="CLOSE GOOD")

        return super().get_new_status(request)

class ReturnPartNoNCM(PendingPartListView):
    query = (
        Q(request_status__pk__gte=9) &
        Q(request_status__pk__lte=10)
    )
    template_name = "pts/return_ta.html"
