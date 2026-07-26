from django.db import models
from django.utils import timezone
from companies.models import Company
from employees.models import Employee


class Payroll(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="payrolls")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payrolls")
    date = models.DateField(default=timezone.now)

    basic_salary = models.DecimalField(max_digits=10, decimal_places=3, editable=False, default=0)
    allowance = models.DecimalField(max_digits=10, decimal_places=3, editable=False, default=0)
    incentives = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=3, editable=False, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=3, editable=False, default=0)

    paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.employee_id:
            self.basic_salary = self.employee.basic_salary or 0
            self.allowance = self.employee.allowance or 0

        self.gross_salary = (
            (self.basic_salary or 0)
            + (self.allowance or 0)
            + (self.incentives or 0)
            + (self.bonus or 0)
        )
        self.net_salary = self.gross_salary - (self.deductions or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} - {self.date}"
