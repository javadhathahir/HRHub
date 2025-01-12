from django.db import models
from django.core.exceptions import ValidationError
from datetime import time
from django.utils import timezone
from employee_management.models import Employee

def validate_time_format(value):
    if value and not isinstance(value, time):
        raise ValidationError('Time must be in HH:MM[:ss[.uuuuuu]] format.')

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    date = models.DateField(default=timezone.now)  # Ensure you store the date
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Field for total hours worked

    # Ensure each employee can only have one attendance record per day
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_attendance_per_day')
        ]

    def __str__(self):
        return f'{self.employee} - {self.date} - {self.status} - {self.total_hours}'
