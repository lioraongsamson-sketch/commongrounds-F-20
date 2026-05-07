from .models import Event, EventSignup
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from accounts.mixins import RoleRequiredMixin
from .forms import EventForm, EventUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        localevent = self.get_object()
        # context['signups'] = localevent.event_signup.all()
        # context['signups'].add(self.request.user.profile)

        # context = super().get_context_data(**kwargs)
        # event = self.get_object()
        # if self.request.user.is_authenticated:
        #     event.signups.add(self.request.user.profile)
        return context


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
        saved_form = super().form_valid(form)
        self.object.organizer.add(self.request.user.profile)
        return saved_form


class EventUpdateView(RoleRequiredMixin, UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = "event_update.html"
    required_role = "Event Organizer"

    def form_valid(self, form):
        event = form.save(commit=False)
        event.update_status()
        event.save()
        return redirect('localevents:event_detail', pk=event.pk)
