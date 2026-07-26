from django import forms
from .models import Document
from employees.models import Employee


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['employee', 'title', 'file', 'expiry_date', 'is_company_document']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        company_id = kwargs.pop('company_id', None)
        super().__init__(*args, **kwargs)

        if company_id:
            self.fields['employee'].queryset = Employee.objects.filter(company_id=company_id)
        else:
            self.fields['employee'].queryset = Employee.objects.none()


class DocumentRenewForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['expiry_date', 'file']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
