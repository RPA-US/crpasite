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
from django.urls import path, include, re_path
import django_cas_ng.views as cas_views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext as _
from django.views.generic import RedirectView
from .settings import prefix_default_language
from airpapi import views

admin.AdminSite.site_title=_("Administración AIRPAPI Web")

#urlpatterns = [
#    #path('admin/', admin.site.urls),
#    re_path(r'^i18n/', include('django.conf.urls.i18n')),
#    re_path(r'^admin/', admin.site.urls),
#    re_path(r'^auth/', include('djoser.urls')),
#    re_path(r'^auth/', include('djoser.urls.authtoken')),
#    re_path(r'^', include('api.urls')) # Added API
#]

urlpatterns = [
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^cas/', include('mama_cas.urls')),
    re_path(r'^admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    re_path(r'^$', views.projects_view, name='home'),
    re_path(r'^accounts/logout/$', cas_views.LogoutView.as_view(), name='cas_ng_logout'),
    re_path(r'^accounts/callback/$', cas_views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
    re_path(r'^admin/login/', RedirectView.as_view(url='/accounts/login/')),
    re_path(r'^admin/logout/', RedirectView.as_view(url='/accounts/logout/')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^register/$', views.register_user, name='register_user'),
    re_path(r'^profile/$', views.profile, name='user_profile'),
    re_path(r'^contact/$', views.contact, name='contact'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^surveys-list/(?P<id_project>\d+)/(?P<id_survey>\d+)$', views.surveys_list_view, name='surveys_list'),
    re_path(r'^recommend-list/(?P<id_project>\d+)/(?P<id_survey>\d+)$', views.recommend_list_view, name='recommend_list'),
    re_path(r'^datasets-list/(?P<id_project>\d+)$', views.datasets_list_view, name='datasets_list'),
    re_path(r'^load-dataset/(?P<source>\w{0,100})/(?P<identifiers>[0-9|nul]+)/(?P<id_project>\d+)$', views.load_dataset_view, name='load_dataset'),
    re_path(r'^models_list/(?P<id_project>\d+)$', views.models_list_view, name='models_list'),
    re_path(r'^manage-project/(?P<id_project>\d+)$', views.manage_project_view, name='manage_project'),
    re_path(r'^delete-project/(?P<id_project>\d+)$', views.delete_project_view, name='delete_project'),
    re_path(r'^accounts/login/$', cas_views.LoginView.as_view(), name='cas_ng_login'),
    re_path(r'^admin/translator/', include('rosetta.urls')),
    re_path(r'^project-status/(?P<id_project>[0-9a-f-]+)$', views.ProjectStatus.as_view(), name='project_status'),
    prefix_default_language=prefix_default_language
)

