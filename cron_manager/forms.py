# forms.py
from django import forms
from .models import ServerCredentials

class ServerCredentialsForm(forms.ModelForm):
    class Meta:
        model = ServerCredentials
        fields = ['hostname', 'username', 'encrypted_password']