# APPs
from systemtest.utils.views import AbstractFilteView
from systemtest.pts import forms as pts_forms


class HistoryPartListView(AbstractFilteView):
    """
    Django ListView for history of parts
        References:
            https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#listview
            https://docs.djangoproject.com/en/3.1/topics/auth/default/#the-permissionrequiredmixin-mixin

    """

    filterset_class = pts_forms.HistoryFilterSet
    template_name = "pts/history.html"
