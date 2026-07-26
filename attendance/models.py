from django.db import models
from companies.models import Company
from employees.models import Employee


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('leave', 'Leave'),
        ('medical_leave', 'Medical Leave'),
        ('earned_leave', 'Earned Leave'),
        ('casual_leave', 'Casual Leave'),
        ('unpaid_leave', 'Unpaid Leave'),
        ('holiday', 'Holiday'),
        ('weekoff', 'Week Off'),
        ('work_from_home', 'Work From Home'),
        ('travel', 'Travel'),
        ('training', 'Training'),
        ('duty_leave', 'Duty Leave'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='attendance_records')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('company', 'employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"


class Overtime(models.Model):
    DAY_TYPE_CHOICES = [
        ('working_day', 'Working Day'),
        ('holiday', 'Holiday'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='overtimes')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='overtimes')
    work_date = models.DateField()
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    day_type = models.CharField(max_length=20, choices=DAY_TYPE_CHOICES)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=3)
    amount = models.DecimalField(max_digits=10, decimal_places=3, editable=False)
    paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('company', 'employee', 'work_date')
        ordering = ['-work_date', '-id']

    def save(self, *args, **kwargs):
        self.amount = (self.hours or 0) * (self.rate_per_hour or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} - {self.work_date} - {self.hours} hrs"
