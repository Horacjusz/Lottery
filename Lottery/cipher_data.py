import json
import os
from cryptography.fernet import Fernet

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")  # Ścieżka do katalogu `data`
KEY_PATH = os.path.join(DATA_PATH, "secret.key")

def generate_key():
    """
    Generuje klucz szyfrowania i zapisuje go do pliku.
    """
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Ładuje klucz szyfrowania z pliku.
    """
    return open(KEY_PATH, "rb").read()

def encrypt_file(data, path):
    """
    Szyfruje dane i zapisuje je do pliku.
    """
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())

    with open(path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(path):
    """
    Odszyfrowuje dane z pliku i zwraca jako słownik.
    """
    key = load_key()
    fernet = Fernet(key)

    with open(path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())
