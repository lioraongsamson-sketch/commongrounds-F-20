from django.shortcuts import render
from .models import Event
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.


class EventListView(ListView):
    model = Event
    template_name = "events_list.html"


class EventDetailView(DetailView):
    model = Event
    template_name = "event.html"
