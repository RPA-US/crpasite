from django.contrib import admin

# Register your models here.
from categories.admin import CategoryBaseAdmin
from .models import TaxCateg, CategoryTerm, Comment, InputFormatSupported, KnowledgeSource, Report

class TaxCategAdmin(CategoryBaseAdmin):
    pass
class CategoryTermAdmin(admin.ModelAdmin):
    pass
class CommentAdmin(admin.ModelAdmin):
    pass
class InputFormatSupportedAdmin(CategoryBaseAdmin):
    pass
class KnowledgeSourceAdmin(admin.ModelAdmin):
    pass
class ReportAdmin(admin.ModelAdmin):
    pass

admin.site.register(TaxCateg, TaxCategAdmin)
admin.site.register(CategoryTerm, CategoryTermAdmin)
admin.site.register(InputFormatSupported, InputFormatSupportedAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(KnowledgeSource, KnowledgeSourceAdmin)