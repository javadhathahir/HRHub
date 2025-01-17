# In payroll/forms.py
from django import forms
from .models import Payroll

class PayrollForm(forms.ModelForm):
    employee = forms.IntegerField(label="Employee ID", required=True)
    payment_date = forms.DateField(label="Payment Date (YYYY-MM-DD)", required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Payroll
        fields = ['employee','payment_date']

    def clean(self):
        cleaned_data = super().clean()
        employee = cleaned_data.get('employee')
        payment_date = cleaned_data.get('payment_date')

        # Check for duplicate payroll entries
        if Payroll.objects.filter(employee=employee, payment_date=payment_date).exists():
            raise forms.ValidationError("Payroll entry for this employee and date already exists.")

        return cleaned_data