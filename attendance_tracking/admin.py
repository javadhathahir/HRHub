from django.contrib import admin
from .models import Attendance

# Register your models here.

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'total_hours')
    search_fields = ('employee', 'date', 'status')
    list_filter = ('employee', 'date', 'status')
