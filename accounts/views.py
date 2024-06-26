# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth import logout

# View for Accounts App
#Register a user
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            # Create a new User instance
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Store success message in session
            messages.success(request, f'User {username} registered successfully. You can now login.')
            
            # Redirect to login page upon successful registration
            return redirect('/')
        else:
            messages.error(request, 'Please provide username, email, and password')
    
    return render(request, 'accounts/register.html')


#User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('cron_manager:cron_manager_home')  # Redirect to cron-manager app
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

#User Logout View.
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')  # Redirect to the login page after logout