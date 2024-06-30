# forms.py
from django import forms
from .models import ServerCredentials

class ServerCredentialsForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput, help_text="Leave blank to keep unchanged")

    class Meta:
        model = ServerCredentials
        fields = ['hostname', 'username']

    def save(self, commit=True):
        server_credential = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            server_credential.set_encrypted_password(password)
        if commit:
            server_credential.save()
        return server_credential