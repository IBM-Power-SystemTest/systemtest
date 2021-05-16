# Django Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# Django filters
from django_filters.views import FilterView

# APPs
from systemtest.utils.forms import PaginationForm


class AbstractFilteView(LoginRequiredMixin, FilterView):
    def get_context_data(self, **kwargs):
        pagination = int(self.request.GET.get("pagination", 10))
        self.paginate_by = pagination

        pagination_form = PaginationForm(
            initial={"pagination": pagination}
        )

        kwargs["pagination_form"] = pagination_form
        kwargs["request"] = self.request

        return super().get_context_data(**kwargs)
