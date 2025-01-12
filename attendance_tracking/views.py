from django.shortcuts import render,redirect #get_object_or_404
from .models import Attendance
from django.contrib.auth.decorators import login_required
#from django.http import JsonResponse
from datetime import time,timedelta
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from employee_management.models import Employee
from django.db import IntegrityError



@login_required
def attendance_report(request):
    attendance_records = Attendance.objects.filter(employee=request.user)
    return render(request, 'attendance_tracking/attendance_report.html', {'records': attendance_records})


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        # Automatically use today's date
        date = timezone.now().date()

        # Get other form data
        status = request.POST.get('status')
        check_in_time = request.POST.get('check_in_time')  # Should be in "HH:MM" format
        check_out_time = request.POST.get('check_out_time')  # Should be in "HH:MM" format

        try:
            # Fetch the Employee instance linked to the logged-in user
            employee = request.user.employee

            # Find or create the attendance record for the current employee and today's date
            attendance, created = Attendance.objects.get_or_create(employee=employee, date=date)

            if status:
                # Save the status when Mark Attendance button is clicked
                attendance.status = status

            if check_in_time and check_out_time:
                try:
                    # Convert string inputs into time objects
                    check_in = time.fromisoformat(check_in_time)
                    check_out = time.fromisoformat(check_out_time)

                    # Calculate total hours worked
                    check_in_delta = timedelta(hours=check_in.hour, minutes=check_in.minute)
                    check_out_delta = timedelta(hours=check_out.hour, minutes=check_out.minute)
                    total_worked = (check_out_delta - check_in_delta).total_seconds() / 3600  # Convert to hours

                    # Save the total hours to the Attendance record
                    attendance.check_in_time = check_in
                    attendance.check_out_time = check_out
                    attendance.total_hours = round(total_worked, 2)
                except ValueError:
                    messages.error(request, "Invalid check-in or check-out time format.")
            
            # Save the attendance record after setting all fields
            attendance.save()
            messages.success(request, "Attendance marked successfully.")
        except Employee.DoesNotExist:
            messages.error(request, "No Employee record found for the logged-in user.")
        
        except IntegrityError:
            messages.error(request, "Attendance for today already exists. Please do not submit again.")
        
        return redirect('attendance_tracking:mark_attendance') 

    return render(request, 'attendance_tracking/mark_attendance.html')







