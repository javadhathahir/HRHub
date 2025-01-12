from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from employee_management.models import Employee

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin list view
    list_display = ('username', 'email', 'employee', 'is_staff', 'is_active','employee_id')
    list_filter = ('is_staff', 'is_active', 'groups')
    
    # Define the fieldsets for the admin form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name', 'employee')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define the add fieldsets for creating new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'employee', 'is_staff', 'is_active')}
        ),
    )
    
    # Add search functionality
    search_fields = ('username', 'email', 'employee__employee_id')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

