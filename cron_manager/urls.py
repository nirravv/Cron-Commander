# cron_manager/urls.py

from django.urls import path
from . import views

app_name = 'cron_manager'

urlpatterns = [
    path('', views.cron_manager_home, name='cron-manager-home'),
]