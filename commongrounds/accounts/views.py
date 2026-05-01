from django.views.generic.edit import UpdateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profile_update.html"
    fields = ['display_name']

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        return get_object_or_404(Profile, user__username=username)


# success_url = "/"
