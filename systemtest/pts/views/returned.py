from typing import Any, Type

# Django HTTP
from django.urls.base import reverse_lazy

# Django db
from django.db.models import Q

# APP PTS
from systemtest.pts import models as pts_models, forms as pts_forms
from .views import BaseRequestListView
from .pending import PendingPartListView


class ReturnPartListView(BaseRequestListView):
    template_name = "pts/return.html"
    success_url = reverse_lazy("pts:return")

    form_class = pts_forms.ReturnFormset

    query = (
        Q(request_status__name="GOOD") |
        Q(request_status__name="BAD")
    )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.user_groups.filter(name="IPIC"):
            self.template_name = "pts/return_ipic.html"

        elif self.user_groups.filter(name="IPIC NCM"):
            self.template_name = "pts/return_ipic_ncm.html"

        elif self.user_groups.filter(name="TA"):
            self.template_name = "pts/return_ta.html"

        return super().get_context_data(**kwargs)

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        if self.user_groups.filter(name="TA"):
            return True
        return super().is_valid_serial(request, serial)

    def get_new_status(self, request: Type[pts_models.Request]) -> Any:
        status = str(request.request_status)
        if self.user_groups.filter(name="TA"):
            self.next_status = request.request_status
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
