from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^user/(?P<username>[-\w]+)/$', views.subscription_user,
        name='api_subscription_user'),
    path(r'', views.subscription_list, name='api_subscription_list'),   
]