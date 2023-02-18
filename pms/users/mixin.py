from users.decorators import inactive_user_not_allow
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ActiveUserRequiredMixin:
    @method_decorator(inactive_user_not_allow)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CustomActiveLoginRequiredMixin(LoginRequiredMixin, ActiveUserRequiredMixin):
    pass
