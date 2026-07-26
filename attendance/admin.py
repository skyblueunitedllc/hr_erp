from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('company', 'employee', 'date', 'status', 'remark')
    list_filter = ('company', 'status', 'date')
    search_fields = ('employee__first_name', 'employee__last_name', 'company__name', 'status')
    ordering = ('-date',)