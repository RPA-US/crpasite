from django.urls import path
from .views import login_page, register_page, guest_register_view, register_page_reviewer
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", login_page, name="login"),
    path("register/", register_page, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("guest/register/", guest_register_view, name="guest_register"),
    path("reviewer/register/", register_page_reviewer, name="reviewer_register"),
]

