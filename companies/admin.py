from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "country", "currency", "is_active", "created_at")
    search_fields = ("name", "code", "country")
    list_filter = ("country", "currency", "is_active")
