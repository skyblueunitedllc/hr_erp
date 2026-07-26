from datetime import date
from django.db import models


class Document(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    expiry_date = models.DateField(blank=True, null=True)
    is_company_document = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def status(self):
        if self.expiry_date:
            if self.expiry_date < date.today():
                return "expired"
            elif (self.expiry_date - date.today()).days <= 30:
                return "expiring"
        return "valid"
