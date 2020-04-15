from django.urls import path, re_path
from api.views import SignUpView, ProfileView
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    # re_path(r'^user/(?P<username>[-\w]+)/$', views.subscription_user,
    #     name='api_subscription_user'),
    # path(r'', views.subscription_list, name='api_subscription_list'),  
]