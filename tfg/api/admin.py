from django.contrib import admin
from .models import Subscription, Service

# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'owner', 'is_public', 'date_updated')
    list_editable = ('is_public',)
    list_filter = ('is_public', 'owner__username')
    search_fields = ['url', 'title', 'description']
    readonly_fields = ('date_created', 'date_updated')

    # list_display: These fields will be shown in the list view.
    # list_editable: These fields are editable in the list view .
    # list_filter: These fields can be filtered in the list view based on their values. The filter items will be shown in a column on the right side.
    # search_fields: These fields can be searched for in the list view based on their values. A search field will be shown above the list.
    # readonly_fields: These fields are not editable in the detail view.

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Service)