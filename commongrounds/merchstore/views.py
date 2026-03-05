from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
# Create your views here.
