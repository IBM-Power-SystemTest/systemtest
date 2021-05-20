
from django.http.response import HttpResponse, HttpResponseRedirect

from django.urls.base import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from systemtest.people import forms as people_forms



class RequestView(LoginRequiredMixin, FormView):
    template_name = "people/request.html"
    success_url = reverse_lazy("people:requirements")
    form_class = people_forms.PeopleRequirementForm

    def dispatch(self, *args, **kwargs):
        user_groups = self.request.user.groups.all()
        if not user_groups.filter(name="LEAD"):
            return HttpResponseRedirect(reverse_lazy("home"))

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        requirement = form.save(commit=False)
        requirement.by_user = self.request.user

        requirement.save()
        return HttpResponseRedirect(self.get_success_url())
