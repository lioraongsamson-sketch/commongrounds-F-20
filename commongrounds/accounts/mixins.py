from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class RoleRequiredMixin(LoginRequiredMixin):
    required_role = None
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not self.has_required_role(request.user):
            return redirect("/accounts/login/")
        return super().dispatch(request, *args, **kwargs)
    
    def has_required_role(self, user):
        if not self.required_role:
            return True
        try:
            return user.profile.role == self.required_role
        except AttributeError:
            return False