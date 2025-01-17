from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from user_auth.models import CustomUser  # Import your custom user model
from employee_management.models import Employee
from django.http import Http404  # Import to raise 404 error if employee is not found


# This view will show the logged-in user's profile data

@login_required
def profile_view(request):
    user = request.user  # Get the logged-in user
    # If the logged-in user is an admin
    if user.is_superuser:
        return render(request, 'user_profile/profile.html', {'user': user,'first_name':'Admin','last_name':'HRHub'})

    
    try:
        # Fetch employee data related to the logged-in user
        employee = Employee.objects.get(user=user)  # Modify this if the relation is different
    except Employee.DoesNotExist:
        # Handle the case where employee does not exist, raise a 404 error
        raise Http404("Employee does not exist.")
    
    # Pass the employee and user data to the template
    return render(request, 'user_profile/profile.html', {
        'user': user,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'employee':employee,
        'profile_picture':employee.profile_picture
    })