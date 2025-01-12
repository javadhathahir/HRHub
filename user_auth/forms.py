from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from employee_management.models import Employee  # Import the Employee model
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    employee_id = forms.CharField(max_length=20, required=True, label="Employee ID")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'employee_id']

    # Validate the employee_id
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get('employee_id')
        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            raise forms.ValidationError("Employee with this ID does not exist.")
        return employee_id

    # Save the user and associate the employee to the user
    def save(self, commit=True):
        user = super().save(commit=False)
        employee_id = self.cleaned_data['employee_id']
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            user.employee = employee  # Assign employee to the user
        except Employee.DoesNotExist:
            raise ValueError("Employee with this ID does not exist.")

        if commit:
            user.save()
        return user
