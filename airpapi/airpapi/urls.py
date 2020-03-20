"""airpapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from processor import views
from rest_framework_swagger.views import get_swagger_view
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger
schema_view = get_swagger_view(title='AIRP@PI documentation')

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
# 
# urlpatterns = [
#     re_path(r'^i18n/', include('django.conf.urls.i18n')),
#     re_path(r'^cas/', include('mama_cas.urls')),
#     re_path(r'^admin/', admin.site.urls),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view),
    re_path(r'^auth/', include('djoser.urls')),
    # re_path(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('v1/api/', include(router.urls)),
]