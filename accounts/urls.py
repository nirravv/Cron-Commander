# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login, name='login'),
    path('user_login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('user_register/', views.user_registration, name='user_register'),
    path('logout/', views.user_logout, name='logout'),
]
