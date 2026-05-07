from .models import Event, EventSignup
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from accounts.mixins import RoleRequiredMixin
from .forms import EventForm, EventUpdateForm
from django.urls import reverse_lazy


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
    group = Event.objects.get(id=1)


class EventSignup(DetailView):
    model = EventSignup
    template_name = "event_signup.html"


class EventCreateView(RoleRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_create.html"
    success_url = reverse_lazy('localevents:event_list')
    required_role = "Event Organizer"

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        return super().form_valid(form)


class EventUpdateView(RoleRequiredMixin, UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = "event_update.html"
    required_role = "Event Organizer"

    def form_valid(self, form):
        event = form.save(commit=False)
        if event.event_signups >= event.event_capacity:
            event.status = 'Full'
        else:
            event.status = 'Available'
        return super().form_valid(form)
