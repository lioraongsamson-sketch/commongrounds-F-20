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
        'accounts.Profile',
        related_name='organizer'
    )
    # https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Models
    # Doesn't have the on delete to null cause this doesn't support it...

    event_image = models.ImageField(
        upload_to='images/', default='.media/images/csci_default_img.png')
    description = models.TextField()
    location = models.CharField()
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    event_capacity = models.PositiveIntegerField(null=True)
    event_signups = models.IntegerField(default=0)
    status_options = [("Available", "Available"), ("Full", "Full"),
                      ("Done", "Done"), ("Cancelled", "Cancelled")]
    # From: https://forum.djangoproject.com/t/django-choices-design/9945
    status = models.CharField(choices=status_options, null=True)
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

    user_registrant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    new_registrant = models.CharField()

    # if request.user.is_authenticated: https://stackoverflow.com/questions/3644902/how-to-check-if-a-user-is-logged-in-how-to-properly-use-user-is-authenticated
