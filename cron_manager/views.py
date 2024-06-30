# cron_manager/views.py

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
import paramiko  # For SSH connection
from paramiko import SSHClient, AutoAddPolicy, SSHException
from datetime import datetime
from django.contrib import messages
from cron_descriptor import get_description
from .models import *
from . forms import ServerCredentialsForm

@login_required
def cron_manager_home(request):
    user_credentials = ServerCredentials.objects.filter(user=request.user)
    return render(request, 'cron_manager/index.html', {'server_credentials': user_credentials})

@login_required
def add_server(request):
    if request.method == 'POST':
        form = ServerCredentialsForm(request.POST)
        if form.is_valid():
            server_credentials = form.save(commit=False)
            server_credentials.user = request.user 
            server_credentials.save()
            messages.success(request, f'{server_credentials.hostname} server\'s credentials added successfully.')
            return redirect('cron_manager:cron_manager_home')
        else:
            messages.error(request, 'Error adding server credentials. Please check the form.')
    else:
        form = ServerCredentialsForm()
    
    return render(request, 'cron_manager/add_server.html', {'form': form})


@login_required
def edit_server(request, credential_id):
    server_credential = ServerCredentials.objects.get(id=credential_id, user=request.user)
    # server_credential = get_object_or_404(ServerCredentials, id=credential_id, user=request.user)
    print(server_credential.encrypted_password)
    form = ServerCredentialsForm(request.POST, instance=server_credential)

    if form.is_valid():
        print(form)
        form.save()
        return redirect('cron_manager:cron_manager_home')

    return render(request, 'cron_manager/edit_server.html', {'server_credential': server_credential})


@login_required
def delete_server_credential(request, credential_id):
    credential = get_object_or_404(ServerCredentials, id=credential_id, user=request.user)
    
    if request.method == 'POST':
        credential.delete()
        return redirect('cron_manager:cron_manager_home')  # Redirect to the home page or any other appropriate page after deletion
    
    # Optionally handle GET request (direct link click) by redirecting or showing a message
    return redirect('cron_manager:cron_manager_home')  # Redirect to the home page if accessed via GET (direct link click)


@login_required
def fetch_cron_jobs(request, server_id):
    
    server = get_object_or_404(ServerCredentials, pk=server_id, user=request.user)

    if request.method == 'POST':
        hostname = server.hostname
        username = server.username
        decrypt_password = server.get_decrypted_password()
        password = decrypt_password  # Assuming you have a field for encrypted password

        try:
            # Establish SSH connection to the server
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(hostname, username=username, password=password, timeout=10)  # Adjust timeout as needed

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

        except SSHException as e:
            # Custom error message for SSH connection issues
            messages.error(request, 'Error connecting to SSH server. Please check your credentials and server availability.')
        except TimeoutError as e:
            # Custom error message for timeout issues
            messages.error(request, 'Connection timed out. Please ensure the server is reachable and try again.')
        except Exception as e:
            # General catch-all error message
            messages.error(request, f'Error: {e}')

    return render(request, 'cron_manager/fetched_cron_jobs.html', {'server': server})