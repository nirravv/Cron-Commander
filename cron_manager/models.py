from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import User


# Ensure you have a key set for Fernet
fernet = Fernet(settings.FERNET_KEY.encode())

class ServerCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    encrypted_password = models.TextField()

    def set_encrypted_password(self, password):
        self.encrypted_password = fernet.encrypt(password.encode()).decode()

    def get_decrypted_password(self):
        return fernet.decrypt(self.encrypted_password.encode()).decode()

    def save(self, *args, **kwargs):
        if not self.pk:  # If object is being created (not updated)
            self.set_encrypted_password(self.encrypted_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.hostname
