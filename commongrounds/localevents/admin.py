from django.contrib import admin
from .models import Event, EventType


class EventInline(admin.TabularInline):
    model = Event


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    inlines = [EventInline,]


admin.site.register(EventType, EventTypeAdmin)
