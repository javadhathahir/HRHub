# In payroll/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Payroll
from .forms import PayrollForm
from employee_management.models import Employee
from attendance_tracking.models import Attendance
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages


from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied




@login_required
@permission_required('payroll.add_payroll', raise_exception=True)
def generate_payroll(request):
    if request.method == 'POST':
       try:
            
            # Retrieve the employee_id and date from POST data
            employee_id = request.POST.get('employee_id')
            date = request.POST.get('date')
           

            # Convert the date string to a Python datetime object
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        
            # Extract the month and year from the date
            month = date_obj.month
            year = date_obj.year

            # Retrieve the employee and basic salary
            employee = Employee.objects.get(id=employee_id)
            basic_salary = employee.basic_salary

            # Assuming 30 days in a month for simplicity
            one_day_basic_salary = basic_salary / 30

            # Count the number of days present in the month
            attendance_count = Attendance.objects.filter(
            employee=employee, 
            date__month=month, 
            date__year=year, 
            status='Present'
            ).count()

            # Calculate the monthly salary
            monthly_salary = one_day_basic_salary * attendance_count

            # Get or create the payroll entry
            payroll_entry, created = Payroll.objects.get_or_create(
            employee=employee,
            
            defaults={'salary': monthly_salary}
            )
        
            if not created:
               payroll_entry.salary = monthly_salary
               payroll_entry.save()

            # Return a success response
            #return HttpResponse(f"Payroll generated for {employee.first_name} {employee.last_name}: {monthly_salary}")
            # Add success message
            messages.success(
               request,
               f"Payroll generated for {employee.first_name} {employee.last_name}: {monthly_salary}"
            )
        
            return redirect('payroll:generate_payroll')
       except ObjectDoesNotExist:
            messages.error(request, "Employee not found.")
            return redirect('payroll:generate_payroll')
       except IntegrityError:
            messages.error(request, "Error occurred while saving payroll.")
            return redirect('payroll:generate_payroll')
       except PermissionDenied:
            messages.error(request, "You do not have permission to generate payroll.")
            return redirect('dashboard:dash_view')
       except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return redirect('payroll:generate_payroll')

    form=PayrollForm()
    # If the request method is GET, render the form page
    return render(request, 'payroll/generate_payroll.html',{'form':form})

@login_required
@permission_required('payroll.view_payroll', raise_exception=True)
def payroll_list(request):
    payrolls = Payroll.objects.all()
    return render(request, 'payroll/payroll_list.html', {'payrolls': payrolls})
