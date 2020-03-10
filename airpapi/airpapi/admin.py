from django.contrib import admin
from .models import WebMicroservices, WebProjects
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from prettyjson import PrettyJSONWidget

# python manage.py createsuperuser --username airpapi --email info.daliasoft@gmail.com --settings=airpapi.settings

admin.site.site_header = 'Administración de AIRPAPI'

# Register your models here.
@admin.register(WebMicroservices)
class WebMicroservicesAdmin(admin.ModelAdmin):
    actions = None
    list_display_links = ('web_tx_name',)
    list_display = ('web_tx_name', 'base_link','admin_link')

    def base_link(self, obj):
        if obj.web_tx_urlbase:
            return "<a href='{0}'>{0}</a>".format(obj.web_tx_urlbase)
        else:
            return
    base_link.short_description = _('URL')
    base_link.allow_tags = True

    def admin_link(self, obj):
        if obj.web_tx_urlbase:
            return "<a href='{0}'>{0}</a>".format(obj.get_admin_url())
        else:
            return
    admin_link.short_description = _('URL de Administración')
    admin_link.allow_tags = True


@admin.register(WebProjects)
class WebProjectsAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('web_tx_name', 'web_cd_user', 'web_tx_status', 'web_tx_identifier')
    readonly_fields = ('web_tx_identifier', 'web_fh_created')
    ordering = ('web_tx_name',)