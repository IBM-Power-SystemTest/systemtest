# Python
from typing import Type

# Django HTTP
from django.urls.base import reverse_lazy

# Django db
from django.db.models import Q

# APP PTS
from .views import BaseRequestListView
from systemtest.pts import models as pts_models


class OpenRequestView(BaseRequestListView):
    template_name = "pts/open.html"
    success_url = reverse_lazy("pts:open")

    query = (
        Q(request_status__pk=1) |
        Q(request_status__pk__gte=10)
    )

    choice_query = Q(pk__gte=10) | Q(pk=1)

    next_status_query = Q(pk=2)

    def get_template_names(self) -> list[str]:
        if self.request.user.groups.filter("IPIC"):
            self.template_name = "pts/open_ipic.html"
        return super().get_template_names()

    def get_new_status(self, request: Type[pts_models.Request]):
        if request.request_group.is_vpd:
            return self.status_model.objects.get(name="GOOD")
        return super().get_new_status(request)

    def is_valid_serial(self, request: Type[pts_models.Request], serial: str) -> bool:
        if serial == request.serial_number:
            return False
        return True
