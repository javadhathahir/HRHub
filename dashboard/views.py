from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee_management.models import Employee
from attendance_tracking.models import Attendance
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Attendance statistics for today (count unique employees with attendance)
from django.db.models import Q  # Ensure this is imported
from user_auth.models import CustomUser



@login_required
def dashboard(request):
    

    # Filtering logic
    employees = Employee.objects.all()
    name_query = request.GET.get('name', '').strip()
    department_query = request.GET.get('department', '').strip()
    role_query = request.GET.get('role', '').strip()

    if name_query:
        employees = employees.filter(first_name__icontains=name_query)
    if department_query:
        employees = employees.filter(department__name__icontains=department_query)
    if role_query:
        employees = employees.filter(role__title__icontains=role_query)

    # Total number of employees
    total_employees = Employee.objects.count()

    # Get today's date
    today = timezone.now().date()

    # Count of employees marked "Present" today
    total_present_today = Attendance.objects.filter(date=today, status='Present').values('employee').distinct().count()

    # Count of employees who have not marked attendance or are "Absent"
    total_absent_today = total_employees - Attendance.objects.filter(date=today).values('employee').distinct().count()

    # Calculate attendance percentage for today
    attendance_percentage_today = (total_present_today / total_employees * 100) if total_employees > 0 else 0

    # Attendance statistics for today (count unique employees with attendance)
    #total_present_today = Attendance.objects.filter(status='Present', date=today).values('employee').distinct().count()
    #total_absent_today = total_employees - total_present_today
    #attendance_percentage_today = (total_present_today / total_employees) * 100 if total_employees > 0 else 0
    
   

    context = {
        'total_employees': total_employees,
        'total_present': total_present_today,
        'total_absent': total_absent_today,
        'attendance_percentage': round(attendance_percentage_today, 2),  # Rounded to 2 decimal places
        'employees': employees,
    }

    return render(request, 'dashboard/dashboard.html', context)





def sidebar(request):
    
    return render(request, 'sidebar.html')

def topbar(request):
    
    return render(request, 'topbar.html')

def footer(request):
    
    return render(request, 'footer.html')

'''@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)  # Fetch the employee object or return 404 if not found
    if request.method == "POST":
        employee.delete()  # Delete the employee record
        return redirect('dashboard:dash_view')  # Redirect to employee list after deletion
    return render(request, 'employee_management/employee_confirm_delete.html', {'employee': employee})  # Render the confirmation modal'''

@login_required
def employee_data(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'dashboard/employee_detail.html', {'employee': employee})





