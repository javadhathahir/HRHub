from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# This view will show the logged-in user's profile data
@login_required
def profile_view(request):
    user = request.user  # Get the logged-in user
    # You can also fetch additional data related to the user if you have a custom user model
    return render(request, 'user_profile/profile.html', {'user': user})
