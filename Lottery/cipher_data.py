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
    Jeśli plik klucza nie istnieje, zwraca None.
    """
    if os.path.exists(KEY_PATH):
        return open(KEY_PATH, "rb").read()
    return None

def ensure_key_exists():
    """
    Sprawdza, czy klucz szyfrowania istnieje, a jeśli nie, generuje go.
    """
    if not os.path.exists(KEY_PATH):
        print("Klucz szyfrowania nie istnieje. Generowanie nowego klucza...")
        generate_key()

def encrypt_file(data, path):
    """
    Szyfruje dane i zapisuje je do pliku.
    """
    # Upewniamy się, że klucz istnieje przed szyfrowaniem
    ensure_key_exists()
    
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
    
    # Sprawdzamy, czy klucz istnieje przed deszyfrowaniem
    if key is None:
        raise FileNotFoundError("Brak klucza szyfrowania. Nie można odszyfrować pliku.")

    fernet = Fernet(key)

    with open(path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())
