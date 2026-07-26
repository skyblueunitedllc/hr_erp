from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_code",
        "first_name",
        "last_name",
        "nationality",
        "department",
        "position",
        "is_active",
    )
    search_fields = (
        "employee_code",
        "first_name",
        "last_name",
        "department",
        "position",
    )
    list_filter = (
        "is_active",
        "nationality",
        "department",
    )
