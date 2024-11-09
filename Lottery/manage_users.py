import os
import json
from cipher_data import decrypt_file, encrypt_file

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")
USERS_FILE = os.path.join(DATA_PATH, "users_encrypted")

def add_user(username, password):
    # Odszyfrowanie istniejących danych użytkowników
    try:
        users_data = decrypt_file(USERS_FILE)
    except FileNotFoundError:
        users_data = {}  # Jeśli plik nie istnieje, tworzymy pusty słownik

    # Sprawdzenie, czy użytkownik już istnieje
    if username in users_data:
        print(f"Użytkownik {username} już istnieje.")
        return

    # Dodanie nowego użytkownika
    users_data[username] = {"password": password}

    # Zaszyfrowanie i zapisanie zaktualizowanych danych użytkowników
    encrypted_data = json.dumps(users_data, ensure_ascii=False, indent=4)
    encrypt_file(encrypted_data, USERS_FILE)
    print(f"Użytkownik {username} został dodany.")

# Przykład użycia
if __name__ == "__main__":
    # Podaj nazwę użytkownika i hasło
    new_username = input("Podaj nazwę użytkownika: ")
    new_password = input("Podaj hasło: ")
    add_user(new_username, new_password)
