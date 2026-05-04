from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Commission


class CommissionListView(ListView):
    model = Commission
    template_name = "request_list.html"
    ordering = ["status", "-created_on"]


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "request_detail.html"


class CommissionCreateView(CreateView):
    model = Commission
    template_name = "request_detail.html"
    fields = '__all__'


class CommissionUpdateView(UpdateView):
    model = Commission
    template_name = "request_detail.html"
    fields = '__all__'
