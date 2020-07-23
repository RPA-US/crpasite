from django.contrib import admin

# Register your models here.
from categories.admin import CategoryBaseAdmin
from .models import TaxCateg

class TaxCategAdmin(CategoryBaseAdmin):
    pass

admin.site.register(TaxCateg, TaxCategAdmin)