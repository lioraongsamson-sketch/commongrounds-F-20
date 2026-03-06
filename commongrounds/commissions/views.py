from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Commission


class CommissionListView(ListView):
    model = Commission
    template_name = "request_list.html"


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "request_detail.html"
