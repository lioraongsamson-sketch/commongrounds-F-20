from functools import wraps
from django.shortcuts import redirect


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or not has_required_role(request.user, required_role):
                return redirect("/accounts/login/")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def has_required_role(user, required_role):
        if not required_role:
            return True
        try:
            return user.profile.role == required_role
        except AttributeError:
            return False