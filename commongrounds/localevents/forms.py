from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'event_image', 'description',
                  'location', 'start_time', 'end_time', 'event_capacity', 'event_signups', 'status']
        widgets = {
            'start_time': forms.TextInput(
                attrs={'type': 'datetime-local'}
            ),
            'end_time': forms.TextInput(
                attrs={'type': 'datetime-local'}
            )
        }


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        # exclude = ('organizer',)
        fields = ['title', 'category', 'event_image', 'description',
                  'location', 'start_time', 'end_time', 'event_capacity', 'event_signups', 'status']
