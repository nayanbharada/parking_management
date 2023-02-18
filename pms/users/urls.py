from django.urls import path
from . import views

# Create your urls here.

app_name = "users"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("register", views.UserCreateView.as_view(), name="register"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("user-dashboard", views.UserDashboard.as_view(), name="user_dashboard"),
    path("admin-dashboard", views.AdminDashboard.as_view(), name="admin_dashboard"),
    path("test", views.AboutUs.as_view(), name="test"),
]
