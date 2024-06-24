# cron_manager/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .decorators import cors  # Import your custom CORS decorator
import paramiko  # For SSH connection

@login_required
def cron_manager_home(request):
    return render(request, 'cron_manager/index.html', {'username': request.user.username})

# Custom CORS decorator to handle CORS headers
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

            # Pass cron_jobs data to the template for rendering
            return render(request, 'cron_manager/fetched_cron_jobs.html', {'cron_jobs': cron_jobs})

        except Exception as e:
            return HttpResponse(f'Error: {e}')

    return HttpResponse(status=405)  # Method Not Allowed
