from cryptography.fernet import Fernet
import base64
import os
from django.conf import settings

# Ensure you have a key set for Fernet
if not hasattr(settings, 'FERNET_KEY'):
    settings.FERNET_KEY = base64.urlsafe_b64encode(os.urandom(32))

fernet = Fernet(settings.FERNET_KEY)

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()
