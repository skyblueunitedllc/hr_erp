from django.db import models
from companies.models import Company


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    employee_code = models.CharField(max_length=20, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    join_date = models.DateField(blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.employee_code:
            company_name = (self.company.name or "").lower()
            if "skyblue" in company_name:
                prefix = "SB"
            elif "fana" in company_name:
                prefix = "FU"
            else:
                prefix = "".join(word[0].upper() for word in self.company.name.split()[:2]) or "EMP"

            last_emp = Employee.objects.filter(company=self.company, employee_code__startswith=prefix).order_by('-id').first()
            next_number = 1
            if last_emp and last_emp.employee_code:
                try:
                    next_number = int(last_emp.employee_code.replace(prefix, "")) + 1
                except ValueError:
                    next_number = 1

            self.employee_code = f"{prefix}{next_number:03d}"

        self.net_salary = (self.basic_salary or 0) + (self.allowance or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_code} - {self.first_name} {self.last_name}"
