from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Print the key
print(key.decode())
