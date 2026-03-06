from django.urls import path
from .views import EventListView, EventDetailView

app_name = 'localevents'

urlpatterns = [
    path('localevents/events', EventListView.as_view(), name='event_list'),
    path(
        'localevents/event/<int:pk>/',
        EventDetailView.as_view(),
        name='event_detail'
    )
]
