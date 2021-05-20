# Django
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

# APPs
from systemtest.people import models as people_models
from systemtest.people.utils.models import get_requirements_summary

class PeopleSummary(TemplateView):
    model = people_models.PeopleRequirement
    template_name = "people/summary.html"

    def get_context_data(self, **kwargs):
        kwargs["summary_list"] = get_requirements_summary()
        return super().get_context_data(**kwargs)
