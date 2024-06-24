# accounts/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .decorators import cors  # Import your custom CORS decorator
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth import logout


# View for rendering HTML pages
def login(request):
    return render(request, 'accounts/login.html')

def register(request):
    return render(request, 'accounts/register.html')

#Register User
# Custom CORS decorator to handle CORS headers
@cors(methods=['POST'])
@csrf_exempt  # Exempt from CSRF protection since we handle it ourselves
@require_http_methods(['POST'])
def user_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            # Create a new User instance
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Store success message in session
            messages.success(request, f'User {username} registered successfully. You can now login.')
            
            # Check if the request is from an API client or frontend GUI
            if request.content_type == 'application/json':
                # Return JSON response for API clients
                return JsonResponse({
                    'username': user.username,
                    'email': user.email
                }, status=201)
            else:
                # Redirect to login page upon successful registration for frontend GUI
                return redirect('/')
        else:
            return JsonResponse({'error': 'Please provide username, email, and password'}, status=400)
    else:
        return HttpResponse(status=405)  # Method Not Allowed

#Login User
@csrf_exempt
@require_http_methods(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('cron_manager:cron_manager_home')  # Redirect to cron-manager app
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def user_logout(request):
    logout(request)
    return redirect('accounts:login')  # Redirect to the login page after logout