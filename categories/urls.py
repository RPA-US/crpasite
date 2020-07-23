from django.urls import path
from accounts.views import login_page, register_page, guest_register_view
from django.contrib.auth.views import LogoutView

app_name = "categories"

urlpatterns = [
    path('navigate/', login_page, name="list"),
    path('proposal/', register_page, name="register"),
    path('review/', LogoutView.as_view(), name="review"),
]