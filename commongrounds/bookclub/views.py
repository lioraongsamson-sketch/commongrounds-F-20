from django.shortcuts import render
from .models import Book
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class BookListView(ListView):
    model = Book


class BookDetailView(DetailView):
    model = Book

# Create your views here.
