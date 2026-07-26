from django.contrib import admin
from .models import Payroll


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'date',
        'basic_salary',
        'allowance',
        'gross_salary',
        'incentives',
        'bonus',
        'deductions',
        'net_salary',
        'paid',
        'paid_date',
    )
    list_filter = ('paid', 'date', 'employee')
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('-date',)
