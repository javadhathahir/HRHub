from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('profile_view/', views.profile_view, name='profile_view'),
    # Add any other URLs related to profile, like updating profile
]
