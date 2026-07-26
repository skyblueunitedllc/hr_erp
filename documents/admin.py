from django.contrib import admin
from django import forms
from .models import Document
from config.forms import MMDDYYYYDateInput

class DocumentAdminForm(forms.ModelForm):
    expiry_date = forms.DateField(
        required=False,
        widget=MMDDYYYYDateInput(),
        input_formats=["%m/%d/%Y"]
    )

    class Meta:
        model = Document
        fields = "__all__"

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ("title", "company", "employee", "expiry_date", "is_company_document", "uploaded_at")
    search_fields = ("title", "company__name", "employee__first_name", "employee__last_name")
    list_filter = ("company", "is_company_document", "expiry_date")
