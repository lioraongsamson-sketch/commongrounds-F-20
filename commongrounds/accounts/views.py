from django.views.generic.edit import UpdateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profile_update.html"
    fields = ['display_name']
#success_url = "/"
