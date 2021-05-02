# Django Views
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Django DB
from django.db.models.query_utils import Q

# Django URLs
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy

# APPs
from systemtest.quality import models as quality_models


class QualityPassed(LoginRequiredMixin, ListView):
    template_name = "quality/passed.html"
    model = quality_models.QualitySystem
    paginate_by = 30
    query = (
        ~Q(operation_status="A") &
        Q(quality_status__name="PASSED")
    )
    queryset = quality_models.QualitySystem.objects.filter(query)


class QualityReturn(DeleteView):
    model = quality_models.QualitySystem
    success_url = reverse_lazy("quality:passed")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.delete()

    def delete(self) -> HttpResponse:
        """
        Change the status of object on the fetched object and then redirect to the
        success URL.
        """
        self.object.quality_status = quality_models.QualityStatus.objects.get(
            name="WAITING")
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
