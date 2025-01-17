"""
URL configuration for HRHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('', include('user_auth.urls')),  # Prefix for user authentication routes
    
    path('dashboard/', include('dashboard.urls')),  # Route for dashboard

    path('employee_management/', include('employee_management.urls')),

    path('attendance_tracking/', include('attendance_tracking.urls')),

    path('user_profile/', include('user_profile.urls')),

     path('payroll/', include('payroll.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)