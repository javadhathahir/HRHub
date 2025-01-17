from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail

from django.contrib.auth.forms import SetPasswordForm
from employee_management.models import Employee 
from .models import CustomUser



def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #return render(request, 'dashboard/dashboard.html')
            return redirect('dashboard:dash_view')  # Replace 'dashboard' with your actual view name
        else:
            return render(request, 'user_auth/login.html', {'error': 'Invalid username or password'})
    return render(request, 'user_auth/login.html')

def user_logout(request):
    logout(request)
    return redirect('user_auth:login')  # Redirect to login page


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dash_view')  # Redirect to the dashboard if the user is already logged in
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id')

        # Validate input fields
        if not username or not password or not email or not employee_id:
            messages.error(request, 'All fields are required.')
            return render(request, 'user_auth/register.html')
        
        # Check if the username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'user_auth/register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return render(request, 'user_auth/register.html')

        # Check if employee ID exists and is not already linked
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            if hasattr(employee, 'user'):
                messages.error(request, 'This employee is already linked to another account.')
                return render(request, 'user_auth/register.html')
        except Employee.DoesNotExist:
            messages.error(request, 'Employee ID does not exist.')
            return render(request, 'user_auth/register.html')

        # Create the user and link to the employee
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            employee=employee  # Assign the employee relationship during creation
        )

        messages.success(request, 'Your account has been created successfully! You can now log in.')
        return redirect('user_auth:login')  # Redirect to the login page after successful registration

    return render(request, 'user_auth/register.html')

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = CustomUser.objects.get(email=email)
                # Generate token for password reset
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())

                
                # Create password reset URL
                reset_url = f"{request.build_absolute_uri('/reset/')}{uid}/{token}/"

                #reset_url = f"{request.build_absolute_uri('/password_reset_confirm/')}{uid}/{token}/"
                message = render_to_string("user_auth/password_reset_email.html", {
                    'user': user,
                    'reset_url': reset_url
                })
                
                # Send the email with the reset URL
                send_mail(
                    "Password Reset Request",
                    message,
                    "admin@example.com",
                    [email],
                )
                
                messages.success(request, "An email with instructions to reset your password has been sent.")
                return redirect('user_auth:password_reset_done')
            except CustomUser.DoesNotExist:
                messages.error(request, "No user found with that email address.")
                return redirect('user_auth:password_reset')
    else:
        form = PasswordResetForm()

    return render(request, "user_auth/password_reset_form.html", {"form": form})




def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        messages.error(request, "The reset link is invalid.")
        return redirect("user_auth:password_reset")

    if default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully!")
                return redirect("user_auth:login")
        else:
            form = SetPasswordForm(user)
            messages.error(request, "Both password should be similar!")
        return render(request, "user_auth/password_reset_confirm.html", {"form": form})
    else:
        messages.error(request, "The reset link is invalid or expired.")
        return redirect("user_auth:password_reset")
    
def password_reset_done(request):
    return render(request, "user_auth/password_reset_done.html")
