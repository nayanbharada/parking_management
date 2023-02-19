from django.shortcuts import render, redirect
from django.views.generic import *

from parking_premises.models import Premises, Slot
from users.forms import LoginForm, CreateUserForm
from django.contrib.auth import authenticate, logout, login
from users.mixin import CustomActiveLoginRequiredMixin
from users.models import UserMaster
from django.contrib import messages


# Create your views here.


class UserCreateView(CreateView):
    template_name = "auth/register.html"
    form_class = CreateUserForm
    success_url = "register"

    def form_valid(self, form):
        form.save(commit=False)
        return super(UserCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "User Is Successfully Created.")
        return self.success_url


class LoginView(View):
    form_class = LoginForm
    template_name = "auth/login.html"

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            if request.user.user_type == UserMaster.ADMIN:
                return redirect("users:admin_dashboard")
            else:
                return redirect("users:user_dashboard")
        else:
            return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.user_type == UserMaster.ADMIN:
                        return redirect("users:admin_dashboard")
                    else:
                        return redirect("users:user_dashboard")
                else:
                    messages.error(request, "your account has been suspended.")
                    return render(request, self.template_name, {"form": form})
            else:
                messages.error(request, "email or password not correct")
                return render(request, self.template_name, {"form": form})
        else:
            return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")


class UserDashboard(CustomActiveLoginRequiredMixin, TemplateView):
    template_name = "dashboards/user_dashboard.html"


class AdminDashboard(CustomActiveLoginRequiredMixin, TemplateView):
    template_name = "dashboards/admin_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(AdminDashboard, self).get_context_data()
        context["premises_count"] = Premises.objects.filter(premise_user=self.request.user).count()
        context["slot_count"] = Slot.objects.filter(premise_slot__premise_user=self.request.user).count()
        return context



