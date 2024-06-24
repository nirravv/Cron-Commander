# cron_manager/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def cron_manager_home(request):
    return render(request, 'cron_manager/home.html', {'username': request.user.username})
