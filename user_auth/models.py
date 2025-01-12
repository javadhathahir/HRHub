from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from employee_management.models import Employee  # Import your Employee model

class CustomUser(AbstractUser):
    # Create a OneToOne relationship with Employee model
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='user', null=True, blank=True)

    # Resolve conflicts by adding unique related_name attributes
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permission_set', blank=True)
