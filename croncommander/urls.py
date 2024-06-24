from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('cron-manager/', include('cron_manager.urls')),  # For cron_manager app URLs
]
