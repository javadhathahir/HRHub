from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Payroll Model
class Payroll(models.Model):
    employee = models.ForeignKey('employee_management.Employee', on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    class Meta:
        unique_together = ('employee', 'payment_date')  # Prevent duplicate payroll entries for the same date

    def __str__(self):
        return f"Payroll for {self.employee} on {self.payment_date}"