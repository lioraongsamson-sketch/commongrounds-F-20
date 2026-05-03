from django.db import models
from django.urls import reverse
from accounts.models import Profile


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'
        ordering = ['name']


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='event'
    )

    organizer = models.ManyToManyField(
        Profile,
        on_delete=models.SET_NULL
    )
    # https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Models

    event_image = models.ImageField()
    description = models.TextField()
    location = models.CharField()
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    event_capacity = models.PositiveIntegerField()
    status_options = [("Available", "Available"), ("Full", "Full"),
                      ("Done", "Done"), ("Cancelled", "Cancelled")]
    # From: https://forum.djangoproject.com/t/django-choices-design/9945
    status = models.CharField(choices=status_options)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_url(self):
        return reverse('localevents:event_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-created_on']


class EventSignup(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        related_name='event_signup'  # Recheck how to properly name this
    )

    # user_registrant = foreign key to profile, model deletion is cascaded,
    # set when registrant is logged in user
    # new_registrant = charfield, set when registrant is not logged in

    new_registrant = models.CharField()
