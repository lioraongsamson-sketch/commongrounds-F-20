from django.urls import path
from .views import EventListView, EventDetailView, EventSignup, EventCreateView, EventUpdateView

app_name = 'localevents'

urlpatterns = [
    path('events', EventListView.as_view(), name='event_list'),
    path('event/add', EventCreateView.as_view(), name="event_create"),
    path('item/<int:pk>/edit', EventUpdateView.as_view(), name="event_update"),
    path(
        'event/<int:pk>/',
        EventDetailView.as_view(),
        name='event_detail'
    ),
    path(
        'event/<int:pk>/signup',
        EventSignup.as_view(),
        name='event_signup'
    )
]
