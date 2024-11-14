from cryptography.fernet import Fernet
from config.settings import CHOOSING_FILE, CHOSEN_FILE, KEY_PATH, USERS_DATA_FILE
import os
import json
from copy import deepcopy
from models.user import User
    
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

def encrypt_data(new_data) :
    encrypt_file(new_data, USERS_DATA_FILE)
    
def decrypt_data(as_dict = False) :
    data_read = decrypt_file(USERS_DATA_FILE)
    if as_dict :
        return data_read
    data = {}
    
    for id in data_read :
        data[id] = User.from_dict(data_read[id])
    
    return data


def update_pool_files(users_data):
    """
    Updates the choosing and chosen files with users marked as choosable.
    """
    
    choosing_data = deepcopy(users_data)
    chosen_data = deepcopy(users_data)

    # Encrypt and save updated choosing and chosen data
    encrypt_file(json.dumps(choosing_data, ensure_ascii=False, indent=4), CHOOSING_FILE)
    encrypt_file(json.dumps(chosen_data, ensure_ascii=False, indent=4), CHOSEN_FILE)