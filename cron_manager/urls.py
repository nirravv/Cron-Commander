# cron_manager/urls.py

from django.urls import path
from . import views

app_name = 'cron_manager'

urlpatterns = [
    path('', views.cron_manager_home, name='cron_manager_home'),
    path('add_server/', views.add_server, name='add_server'),
    path('delete_server_credential/<int:credential_id>/', views.delete_server_credential, name='delete_server_credential'),
    path('fetch_cron_jobs/<int:server_id>/', views.fetch_cron_jobs, name='fetch_cron_jobs'),
]