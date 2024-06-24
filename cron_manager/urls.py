# cron_manager/urls.py

from django.urls import path
from . import views

app_name = 'cron_manager'

urlpatterns = [
    path('', views.cron_manager_home, name='cron_manager_home'),
    path('add_server/', views.add_server, name='add_server'),
    path('add_server_api/', views.add_server_api, name='add_server_api'),
    path('fetch_cron_jobs/', views.fetch_cron_jobs, name='fetch_cron_jobs'),
]