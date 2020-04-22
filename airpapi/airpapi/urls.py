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
from consumer import views as consumer_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from rest_framework_swagger.views import get_swagger_view
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger: schema_view = get_swagger_view(title='AIRP@PI documentation')

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# urlpatterns = [
#     re_path(r'^i18n/', include('django.conf.urls.i18n')),
#     re_path(r'^cas/', include('mama_cas.urls')),
#     re_path(r'^admin/', admin.site.urls),
# ]

schema_view = get_schema_view(
   openapi.Info(
      title="AIRP@PI API",
      default_version='v1',
      description="AI-RPA API platform",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="antmarroj@us.es"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    re_path(r'^scale/text', consumer_views.text_classification, name='text-classification'),
    re_path(r'^scale/image', consumer_views.image, name='image'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # path('docs/', schema_view),
    # path('v1/api', include(router.urls)),
    # re_path(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
]