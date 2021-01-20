from django.views.generic import ListView, FormView, DetailView, CreateView

class TransitPartListView(ListView):
    template_name = "pts/transit.html"
