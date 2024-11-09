import json
import os
from cipher_data import encrypt_file, decrypt_file

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(SCRIPT_PATH, "data")  # Ścieżka do katalogu `data`

def data_initialize():
    """
    Funkcja inicjalizująca cztery zaszyfrowane puste pliki słowników:
    family_data, chosen_data, choosing_data i assignment.
    """
    # Tworzenie pustych słowników
    family_data = {}
    chosen_data = {}
    choosing_data = {}
    assignment = {}

    # Serializacja i zaszyfrowanie każdego słownika
    encrypt_file(json.dumps(family_data), os.path.join(DATA_PATH, "family_data_encrypted"))
    encrypt_file(json.dumps(chosen_data), os.path.join(DATA_PATH, "chosen_encrypted"))
    encrypt_file(json.dumps(choosing_data), os.path.join(DATA_PATH, "choosing_encrypted"))
    encrypt_file(json.dumps(assignment), os.path.join(DATA_PATH, "assignment_encrypted"))
    
    print("Zaszyfrowane pliki family_data_encrypted, chosen_encrypted, choosing_encrypted i assignment_encrypted zostały utworzone.")

def add_person(person_data):
    """
    Funkcja dodająca nową osobę do istniejących zaszyfrowanych plików family_data, chosen_data, choosing_data i assignment.
    """
    # Odszyfrowanie istniejących plików
    family_data = decrypt_file(os.path.join(DATA_PATH, "family_data_encrypted"))
    chosen_data = decrypt_file(os.path.join(DATA_PATH, "chosen_encrypted"))
    choosing_data = decrypt_file(os.path.join(DATA_PATH, "choosing_encrypted"))
    assignment = decrypt_file(os.path.join(DATA_PATH, "assignment_encrypted"))

    # Dodanie nowej osoby do family_data
    person_id = person_data["id"]
    family_data[person_id] = {
        "name": person_data["name"],
        "spouse": person_data.get("spouse"),
        "wishlist": person_data.get("wishlist", [])
    }

    # Jeśli małżonek jest podany, sprawdzenie, czy istnieje w family_data
    spouse_name = person_data.get("spouse")
    if spouse_name:
        for member_id, member_data in family_data.items():
            if member_data["name"] == spouse_name:
                # Aktualizacja małżonka istniejącej osoby
                family_data[member_id]["spouse"] = person_data["name"]
                print(f"Zaktualizowano małżonka dla {spouse_name} jako {person_data['name']}")

    # Aktualizacja chosen_data, choosing_data i assignment
    chosen_data[person_id] = person_data["name"]
    choosing_data[person_id] = person_data["name"]
    assignment[person_id] = None  # Inicjalizujemy przypisanie jako None dla nowej osoby

    # Serializacja i zaszyfrowanie zaktualizowanych słowników
    encrypt_file(json.dumps(family_data, ensure_ascii=False, indent=4), os.path.join(DATA_PATH, "family_data_encrypted"))
    encrypt_file(json.dumps(chosen_data, ensure_ascii=False, indent=4), os.path.join(DATA_PATH, "chosen_encrypted"))
    encrypt_file(json.dumps(choosing_data, ensure_ascii=False, indent=4), os.path.join(DATA_PATH, "choosing_encrypted"))
    encrypt_file(json.dumps(assignment, ensure_ascii=False, indent=4), os.path.join(DATA_PATH, "assignment_encrypted"))
    
    print(f"Osoba {person_data['name']} została dodana do plików family_data_encrypted, chosen_encrypted, choosing_encrypted i assignment_encrypted.")
