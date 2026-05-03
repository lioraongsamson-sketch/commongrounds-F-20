from .models import Event, EventSignup
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class EventListView(ListView):
    model = Event
    template_name = "events_list.html"

    # def post(self, request, *args, **kwargs):
    #    t = Event()
    #    t.title = request.POST.get('event_name')
    #    t.start_time = request.POST.get('start_time')
    #    t.save()

    #    return self.get(request, *args, **kwargs)


class EventDetailView(DetailView):
    model = Event
    template_name = "event.html"


class EventSignup(DetailView):
    model = EventSignup
    template_name = "event_signup.html"
