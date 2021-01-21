# Django
from django.views.generic.detail import DetailView

# APPS
from systemtest.pts import models as pts_models


class DetailRequestView(DetailView):
    model = pts_models.Request
    template_name = "pts/detail.html"
