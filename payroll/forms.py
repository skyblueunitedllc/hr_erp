from django import forms
from .models import Payroll
from employees.models import Employee


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee',
            'date',
            'incentives',
            'bonus',
            'deductions',
        ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'incentives': forms.NumberInput(attrs={'class': 'form-control'}),
            'bonus': forms.NumberInput(attrs={'class': 'form-control'}),
            'deductions': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        company_id = kwargs.pop('company_id', None)
        super().__init__(*args, **kwargs)

        if company_id:
            self.fields['employee'].queryset = Employee.objects.filter(
                company_id=company_id,
                is_active=True
            ).order_by('first_name', 'last_name')
        else:
            self.fields['employee'].queryset = Employee.objects.none()
