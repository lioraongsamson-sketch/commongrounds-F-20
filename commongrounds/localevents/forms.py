from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'organizer', 'event_image', 'description',
                  'location', 'start_time', 'end_time', 'event_capacity', 'status']
        widgets = {
            'start_time': forms.TextInput(
                attrs={'type': 'datetime-local'}
            ),
            'end_time': forms.TextInput(
                attrs={'type': 'datetime-local'}
            ),
            'organizer': forms.Select(attrs={'disabled': 'disabled'}),
        }


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'event_image', 'description',
                  'location', 'start_time', 'end_time', 'event_capacity', 'status']
