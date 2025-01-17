from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
   
    path('generate/', views.generate_payroll, name='generate_payroll'),
    path('list/', views.payroll_list, name='payroll_list'),
]
