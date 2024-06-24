# cron_manager/views.py

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .decorators import cors  # Import your custom CORS decorator
import paramiko  # For SSH connection
from datetime import datetime
from cron_descriptor import get_description
from .models import *
from . forms import ServerCredentialsForm

@login_required
def cron_manager_home(request):
    user_credentials = ServerCredentials.objects.filter(user=request.user)
    return render(request, 'cron_manager/index.html', {'server_credentials': user_credentials})


# Custom CORS decorator to handle CORS headers
@login_required
@cors(methods=['POST'])
@csrf_exempt  # Exempt from CSRF protection since we handle it ourselves
@require_http_methods(['POST'])
def fetch_cron_jobs(request):
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Establish SSH connection to the server
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, username=username, password=password)

            # Execute command to fetch cron jobs
            stdin, stdout, stderr = client.exec_command('crontab -l')

            # Read and decode cron jobs output
            cron_jobs = stdout.read().decode('utf-8')

            # Close SSH connection
            client.close()

            formatted_jobs = []
            for line in cron_jobs.splitlines():
                if line.strip() and not line.strip().startswith('#'):
                    # Parse cron schedule
                    schedule_fields = line.strip().split()
                    cron_expression = ' '.join(schedule_fields[:5])
                    command = ' '.join(schedule_fields[5:])

                    # Use cron-descriptor to get a human-readable description
                    description = get_description(cron_expression)

                    formatted_jobs.append({
                        'description': description,
                        'command': command
                    })

            # Pass cron_jobs data to the template for rendering
            return render(request, 'cron_manager/fetched_cron_jobs.html', {'formatted_jobs': formatted_jobs})

        except Exception as e:
            return HttpResponse(f'Error: {e}')

    return HttpResponse(status=405)  # Method Not Allowed

#Render HTML Page to User.
def add_server(request):
    return render(request, 'cron_manager/add_server.html')

@csrf_exempt
@require_http_methods(['POST'])
@cors(methods=['POST'])
def add_server_api(request):
    if request.method == 'POST':
        form = ServerCredentialsForm(request.POST)
        if form.is_valid():
            server_credentials = form.save(commit=False)
            server_credentials.user = request.user
            server_credentials.save()
            # Check if the request is from an API client
            if request.content_type == 'application/json':
                return JsonResponse({'status': 'success'}, status=201)
            else:
                # Redirect to another URL upon successful creation for frontend GUI
                return redirect('cron_manager:cron_manager_home')
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)