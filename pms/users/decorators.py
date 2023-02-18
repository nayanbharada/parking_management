from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def inactive_user_not_allow(function):
    """for giving permission to the user"""

    def get(request, *args, **kwargs):
        if request.user.is_active:
            return function(request, *args, **kwargs)
        else:
            return redirect("main:logout")

    return get
