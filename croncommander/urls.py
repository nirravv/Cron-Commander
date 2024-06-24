from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')), # For Accounts app URLs
    path('cron_manager/', include('cron_manager.urls')),  # For cron_manager app URLs
]
