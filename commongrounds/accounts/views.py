from django.shortcuts import render
from django.views.generic.edit import UpdateView
from .models import Profile


class ProfileUpdateView(UpdateView):
    model = Event
    template_name = "event.html"

# Create your views here.
