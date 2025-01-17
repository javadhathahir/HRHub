from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Department, Role, EmploymentHistory, Document
from .forms import EmployeeForm, DepartmentForm, RoleForm, EmploymentHistoryForm, DocumentForm

from django.contrib.auth.decorators import login_required, permission_required


# Employee views
@login_required
@permission_required('employee_management.employee_list', raise_exception=True)
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_management/employee_list.html', {'employees': employees})

@login_required
@permission_required('employee_management.employee_detail', raise_exception=True)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee_management/employee_detail.html', {'employee': employee})


@login_required
@permission_required('employee_management.employee_create', raise_exception=True)
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the employee object
            employee = form.save()

            # Ensure the employee_id is generated if it's not already set
            if not employee.employee_id:
                employee.save()  # This will trigger the save method and generate the employee_id

            # Redirect to the employee list or show employee_id to the user
            return redirect('employee_management:employee_list')  # or pass employee_id to the template
    else:
        form = EmployeeForm()

    return render(request, 'employee_management/employee_form.html', {'form': form})


@login_required
@permission_required('employee_management.employee_update', raise_exception=True)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_management:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_management/employee_form.html', {'form': form})

@login_required
@permission_required('employee_management.employee_delete', raise_exception=True)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)  # Fetch the employee object or return 404 if not found
    if request.method == "POST":
        employee.delete()  # Delete the employee record
        return redirect('employee_management:employee_list')  # Redirect to employee list after deletion
    return render(request, 'employee_management/employee_confirm_delete.html', {'employee': employee})  # Render the confirmation modal


