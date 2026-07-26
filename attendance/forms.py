from django import forms
from .models import Attendance, Overtime


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'remark']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OvertimeForm(forms.ModelForm):
    class Meta:
        model = Overtime
        fields = ['employee', 'work_date', 'hours', 'day_type', 'rate_per_hour', 'remark']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'work_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'day_type': forms.Select(attrs={'class': 'form-select'}),
            'rate_per_hour': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
