# Django filters
from systemtest.utils.views import AbstractFilteView

# APPs
from systemtest.quality import forms

class QualityHistory(AbstractFilteView):
    """
    Django ListView for history of systems
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin
    """

    filterset_class = forms.SystemHistoryFilterSet
    template_name = "quality/history.html"
