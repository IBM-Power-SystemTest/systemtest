# Django
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

# APPs
from systemtest.people import models as people_models, forms as people_forms
from systemtest.people.utils.models import get_requirements_summary, get_users_department
from systemtest.utils.views import AbstractFilteView


class PeopleSummary(AbstractFilteView):
    """
    Django ListView for history of systems
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin
    """

    model = people_models.PeopleRequirement
    template_name = "people/summary.html"

    filterset_class = people_forms.PeopleUserFilterSet

    queryset = get_users_department("PRUEBAS")
    ordering = ["username"]


    def get_context_data(self, **kwargs):
        kwargs["summary_dict"] = get_requirements_summary()
        return super().get_context_data(**kwargs)
